-- The UWM CO-OP form: its choices must end up as the same requests the old step-by-step wizard sent.
local A = UWMManager.ACTION
local F = UWMWizard.FORM
local passed, failed = 0, 0
local function check(name, cond, info)
    if cond then passed = passed + 1 print("PASS " .. name)
    else failed = failed + 1 print("FAIL " .. name .. (info and ("  " .. tostring(info)) or "")) end
end
local function near(a, b) return math.abs(a - b) < 0.01 end
local function lastDialog() return dialogLog[#dialogLog] end

-- farm 1 (manager user 10) is the local player, owns the depot; farms 2 and 3 are members
g_currentMission.placeableSystem.placeables = {}
for _, f in pairs(farms) do f.money = 10000 end
PlayerTradingPlus:loadMap("")
local M = PlayerTradingPlus.manager
removeDepots()
newDepot(1, 0)
M.members[2] = UWMManager.newMember(UWMManager.MEMBER.MEMBER)
M.members[3] = UWMManager.newMember(UWMManager.MEMBER.MEMBER)
PlayerTradingPlus.getLocalFarmId = function() return 1 end
table.insert(g_currentMission.placeableSystem.placeables,
    newPlaceable(1, "spec_silo", {storages = {newStorage({[FillType.LIQUIDMANURE] = 50000, [FillType.MANURE] = 0}, 100000)}}))
table.insert(g_currentMission.placeableSystem.placeables,
    newPlaceable(2, "spec_silo", {storages = {newStorage({[FillType.LIQUIDMANURE] = 20000, [FillType.MANURE] = 0}, 100000)}}))

local sent = {}
UWMRequestEvent.sendRequest = function(action, data) table.insert(sent, {action = action, data = data}) end
local function form(mode, other, ft, liters, price, rep, all, discount)
    return {mode = mode, otherFarmId = other, fillTypeIndex = ft, liters = liters, pricePer1000 = price, repeatDays = rep, amountAll = all,
        discountPercent = discount}
end

-- what's missing
check("form: invoice without a farm is refused", UWMWizard.getFormError(form(F.BILL, nil, FillType.LIQUIDMANURE, 1000, 5)) == "uwm_error_formNoFarm")
check("form: standing order needs no farm", UWMWizard.getFormError(form(F.OFFER, nil, FillType.LIQUIDMANURE, 1000, 5)) == nil)
check("form: unknown goods refused", UWMWizard.getFormError(form(F.BILL, 2, FillType.UNKNOWN, 1000, 5)) == "uwm_error_formNoGood")
check("form: no amount refused", UWMWizard.getFormError(form(F.BILL, 2, FillType.LIQUIDMANURE, nil, 5)) == "uwm_error_badAmount")
check("form: 'all in stock' needs no amount on an invoice", UWMWizard.getFormError(form(F.REQUEST, 2, FillType.LIQUIDMANURE, nil, 5, 0, true)) == nil)
check("form: 'all in stock' not allowed on a standing order", UWMWizard.getFormError(form(F.WANTED, nil, FillType.LIQUIDMANURE, nil, 5, 0, true)) == "uwm_error_badAmount")
check("form: negative price refused", UWMWizard.getFormError(form(F.BILL, 2, FillType.LIQUIDMANURE, 1000, -1)) == "uwm_error_badPrice")
dialogLog = {}
check("form: a refused form sends nothing", UWMWizard.startForm(form(F.BILL, nil, FillType.LIQUIDMANURE, 1000, 5)) == nil
    and #sent == 0 and lastDialog().kind == "info")

-- invoice a farm: we sell, weekly
dialogLog, sent = {}, {}
UWMWizard.startForm(form(F.BILL, 2, FillType.LIQUIDMANURE, 10000, 8, UWMInvoice.REPEAT_WEEKLY))
local d = lastDialog()
check("bill: goes straight to the confirm box", d ~= nil and d.kind == "yesno")
d.args[1](d.args[2], true)
local r = sent[1]
check("bill: sends CREATE seller 1 -> buyer 2", r ~= nil and r.action == A.CREATE and r.data.invoice.sellerFarmId == 1
    and r.data.invoice.buyerFarmId == 2 and r.data.invoice.repeatDays == 7 and near(r.data.invoice.liters, 10000)
    and r.data.invoice.amountMode == UWMInvoice.AMOUNT.FIXED)
local ok = M:handleRequest(A.CREATE, 10, {invoice = r.data.invoice})
check("bill: the server takes it as a normal invoice", ok and M.invoices[#M.invoices].sellerFarmId == 1)

-- request an invoice: we buy all their slurry, reserve it
dialogLog, sent = {}, {}
UWMWizard.startForm(form(F.REQUEST, 2, FillType.LIQUIDMANURE, nil, 6, 0, true))
d = lastDialog()
check("request: no reserve question any more, straight to the confirm box", d.kind == "yesno")
d.args[1](d.args[2], true)
r = sent[1]
check("request: sends CREATE seller 2 -> buyer 1, all of it", r ~= nil and r.data.invoice.sellerFarmId == 2
    and r.data.invoice.buyerFarmId == 1 and r.data.invoice.amountMode == UWMInvoice.AMOUNT.ALL)

-- standing sell order
dialogLog, sent = {}, {}
UWMWizard.startForm(form(F.OFFER, nil, FillType.LIQUIDMANURE, 30000, 7))
d = lastDialog()
d.args[1](d.args[2], true)
r = sent[1]
check("sell order: posts an OFFER listing", r ~= nil and r.action == A.POST_LISTING and r.data.listing.kind == UWMListing.KIND.OFFER
    and near(r.data.listing.liters, 30000) and near(r.data.listing.pricePer1000, 7))
ok = M:handleRequest(A.POST_LISTING, 10, {listing = r.data.listing})
check("sell order: the server posts it", ok and M.listings[#M.listings].farmId == 1)

-- standing buy order of electricity: asks for our productions first (none here -> told so, nothing sent)
dialogLog, sent = {}, {}
UWMWizard.startForm(form(F.WANTED, nil, FillType.ELECTRICCHARGE, 100000, 180))
check("buy order of electricity: asks for the productions, none -> message, nothing sent", lastDialog().kind == "info" and #sent == 0)

-- standing buy order of manure
dialogLog, sent = {}, {}
UWMWizard.startForm(form(F.WANTED, nil, FillType.MANURE, 5000, 12))
d = lastDialog()
d.args[1](d.args[2], true)
check("buy order: posts a WANTED listing", sent[1] ~= nil and sent[1].data.listing.kind == UWMListing.KIND.WANTED)

-- what the form shows
check("form: farms list leaves out our own farm", #UWMOrderDialog.getFarms(1) == 2 and UWMOrderDialog.getFarms(1)[1].farmId == 2)
check("form: seller is us on a bill / offer, them on a request, nobody on a buy order",
    UWMOrderDialog.getSellerFarmId(F.BILL, 1, 2) == 1 and UWMOrderDialog.getSellerFarmId(F.OFFER, 1, nil) == 1
    and UWMOrderDialog.getSellerFarmId(F.REQUEST, 1, 2) == 2 and UWMOrderDialog.getSellerFarmId(F.WANTED, 1, nil) == nil)
local name, rows, note = UWMOrderDialog.getPickupInfo(F.REQUEST, 2, FillType.LIQUIDMANURE)
check("pickup: always the depot on the map", name == "Community Depot", name)
check("pickup: owner Community + slurry lane + the seller's stock", #rows == 5 and rows[1][2] == "Community" and rows[2][2] == "Slurry lane (tank)"
    and rows[3][1] == "Seller's stock" and rows[3][2] == "20000" and rows[5][2] == "20000", rows[3] and rows[3][2])
local _, sellRows = UWMOrderDialog.getPickupInfo(F.BILL, 1, FillType.LIQUIDMANURE)
check("pickup: the 10000 bill + 30000 sell order left the farm and wait in the depot", sellRows[3][2] == "10000"
    and sellRows[4][1] == "At the depot for sale" and sellRows[4][2] == "40000", sellRows[3][2] .. " / " .. sellRows[4][2])
local _, wantRows = UWMOrderDialog.getPickupInfo(F.WANTED, nil, FillType.MANURE)
check("pickup: buy order shows no stock rows, manure pit entrance", #wantRows == 2 and wantRows[2][2] == "Manure pit entrance")
local _, powerRows, powerNote = UWMOrderDialog.getPickupInfo(F.BILL, 1, FillType.ELECTRICCHARGE)
check("pickup: electricity is delivered directly", powerRows[2][2] == "Delivered directly" and powerNote:find("no pickup", 1, true) ~= nil)
check("total: liters x price / 1000", near((UWMOrderDialog.getTotals(form(F.BILL, 2, FillType.LIQUIDMANURE, 50000, 8))), 400))
check("total: unknown for 'all in stock'", UWMOrderDialog.getTotals(form(F.BILL, 2, FillType.LIQUIDMANURE, nil, 8, 0, true)) == nil)

-- discount (option 2: stored on the invoice, both farms see it)
check("discount: 100 % or more refused", UWMWizard.getFormError(form(F.BILL, 2, FillType.LIQUIDMANURE, 1000, 5, 0, false, 100)) == "uwm_error_badDiscount")
check("discount: negative refused", UWMWizard.getFormError(form(F.BILL, 2, FillType.LIQUIDMANURE, 1000, 5, 0, false, -5)) == "uwm_error_badDiscount")
local paid, full, off = UWMOrderDialog.getTotals(form(F.BILL, 2, FillType.LIQUIDMANURE, 10000, 33, 0, false, 10))
check("discount: form total 330 - 10 % = 297", near(paid, 297) and near(full, 330) and near(off, 33))
dialogLog, sent = {}, {}
UWMWizard.startForm(form(F.BILL, 2, FillType.LIQUIDMANURE, 10000, 33, 0, false, 10))
d = lastDialog()
check("discount: confirm box shows it", d.kind == "yesno" and d.args[3]:find("10 %", 1, true) ~= nil, d.args[3])
d.args[1](d.args[2], true)
check("discount: travels with the CREATE request", sent[1] ~= nil and sent[1].data.invoice.discountPercent == 10)
for _, f in pairs(farms) do f.money = 10000 end
local before = #M.invoices
ok = M:handleRequest(A.CREATE, 10, {invoice = sent[1].data.invoice})
local inv = M.invoices[#M.invoices]
check("discount: server keeps full price and discount", ok and #M.invoices == before + 1 and inv.discountPercent == 10 and near(inv.pricePer1000, 33))
local seller0, buyer0 = farms[1].money, farms[2].money
notifications, notificationDetails = {}, {}
ok = M:handleRequest(A.ACCEPT, 20, {invoiceId = inv.id})
local sawNotice = false
for i, n in ipairs(notifications) do
    if n == "1:uwm_notify_acceptedDiscount" and notificationDetails[i] == "10 % off" then sawNotice = true end
end
check("discount: the seller's 'accepted' notice says 10 % off", sawNotice, table.concat(notifications, " "))
check("discount: buyer pays 297, seller gets 297", ok and near(buyer0 - farms[2].money, 297) and near(farms[1].money - seller0, 297),
    tostring(buyer0 - farms[2].money))
local sellerText = UWMFrame.getDetailsText(inv, 1)
local buyerText = UWMFrame.getDetailsText(inv, 2)
check("discount: seller's details show percent and money", sellerText:find("10 %", 1, true) ~= nil and sellerText:find("33", 1, true) ~= nil, sellerText)
check("discount: buyer's details say what they saved", buyerText:find("save", 1, true) ~= nil and buyerText:find("297", 1, true) ~= nil, buyerText)
check("discount: list description shows it", UWMFrame.getDescriptionText(inv, 2):find("10 %", 1, true) ~= nil)
check("discount: receipt line shows it", UWMManager.getReceiptLine(inv):find("10 %", 1, true) ~= nil, UWMManager.getReceiptLine(inv))
local copy = UWMInvoice.new()
local xml = XMLFile.create and XMLFile.create("t", "", "root") or nil
if xml ~= nil then
    inv:saveToXMLFile(xml, "root.i") copy:loadFromXMLFile(xml, "root.i")
    check("discount: saved and loaded", copy.discountPercent == 10)
end
check("discount: old invoices have none", UWMInvoice.new().discountPercent == 0)

-- a request: the buyer can't set a discount, the seller gives it when approving (user, 2026-11-02)
check("request: form has no discount box", not UWMWizard.getFormHasDiscount(F.REQUEST) and not UWMWizard.getFormHasDiscount(F.WANTED)
    and UWMWizard.getFormHasDiscount(F.BILL) and UWMWizard.getFormHasDiscount(F.OFFER))
local rq = UWMInvoice.new()
rq.sellerFarmId, rq.buyerFarmId, rq.fillTypeIndex = 1, 2, FillType.LIQUIDMANURE
rq.amountMode, rq.liters, rq.pricePer1000, rq.repeatDays, rq.discountPercent = UWMInvoice.AMOUNT.FIXED, 10000, 20, 0, 5
ok, key = M:handleRequest(A.CREATE, 20, {invoice = rq})
check("request: the server refuses a discount from the buyer", not ok and key == "uwm_error_badDiscount", key)
rq.discountPercent = 0
table.insert(g_currentMission.placeableSystem.placeables,
    newPlaceable(1, "spec_silo", {storages = {newStorage({[FillType.LIQUIDMANURE] = 50000}, 100000)}}))
ok = M:handleRequest(A.CREATE, 20, {invoice = rq})
local req = M.invoices[#M.invoices]
dialogLog = {}
UWMApproveDialog.instance = nil
check("request: the seller's accept opens the approve window", ok and pcall(UWMWizard.startAccept, req))
local ad = UWMApproveDialog.new()
ad.invoice = req
local rpaid, rfull, roff = UWMApproveDialog.getTotals(req, 5)
check("request: approve window total 200 - 5 % = 190", near(rpaid, 190) and near(rfull, 200) and near(roff, 10))
ok, key = M:handleRequest(A.ACCEPT, 10, {invoiceId = req.id, discountPercent = 100})
check("request: 100 % refused when approving", not ok and key == "uwm_error_badDiscount" and req.discountPercent == 0, key)
seller0, buyer0 = farms[1].money, farms[2].money
ok, key = M:handleRequest(A.ACCEPT, 10, {invoiceId = req.id, discountPercent = 5})
check("request: approved with 5 %, buyer pays 190", ok and req.discountPercent == 5 and near(buyer0 - farms[2].money, 190)
    and near(farms[1].money - seller0, 190), key)

print(string.format("form: %d passed, %d failed", passed, failed))
return failed
