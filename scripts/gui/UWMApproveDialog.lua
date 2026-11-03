-- Player Trading+: the seller approves a request for an invoice (another farm asked to buy) and may
-- give a discount (user, 2026-11-02: the seller sets it, not the farm asking). Approve -> ACCEPT with discountPercent.
-- Author: PropaineX

UWMApproveDialog = {}
local UWMApproveDialog_mt = Class(UWMApproveDialog, MessageDialog)

UWMApproveDialog.NAME = "UWMApproveDialog"

local function getText(key)
    return PlayerTradingPlus.getText(key)
end

local function parseNumber(text)
    if text == nil then
        return nil
    end
    return tonumber((text:gsub("[%s,'%%]", "")))
end

function UWMApproveDialog.new(target, customMt)
    return MessageDialog.new(target, customMt or UWMApproveDialog_mt)
end

function UWMApproveDialog.register()
    local dialog = UWMApproveDialog.new()
    g_gui:loadGui(PlayerTradingPlus.modDirectory .. "gui/UWMApproveDialog.xml", UWMApproveDialog.NAME, dialog)
    UWMApproveDialog.instance = dialog
end

function UWMApproveDialog.show(invoice)
    local dialog = UWMApproveDialog.instance
    if dialog == nil then
        return
    end
    dialog.invoice = invoice
    g_gui:showDialog(UWMApproveDialog.NAME)
end

function UWMApproveDialog:onGuiSetupFinished()
    UWMApproveDialog:superClass().onGuiSetupFinished(self)
    UWMGui.applyStaticImages(self.dialogElement)
    if self.headIcon ~= nil and self.headIcon.setImageFilename ~= nil then
        self.headIcon:setImageFilename(PlayerTradingPlus.modDirectory .. UWMFrame.ICON_FILENAME)
        self.headIcon:setImageUVs(nil, unpack(UWMFrame.getIconUVs()))
    end
end

function UWMApproveDialog:onOpen()
    UWMApproveDialog:superClass().onOpen(self)
    local invoice = self.invoice
    if invoice == nil then
        return
    end
    local UWM = PlayerTradingPlus
    local ft = invoice.fillTypeIndex
    local buyerName = UWMManager.getFarmName(invoice.buyerFarmId)

    self.fromText:setText(string.format(getText("uwm_approve_from"), buyerName))
    UWMGui.setIcon(self.goodsIcon, UWMGui.getGoodsIcon(ft, invoice.isPallet))
    local amount = invoice.amountMode == UWMInvoice.AMOUNT.ALL and getText("uwm_summary_amountAll")
        or UWM.formatAmount(ft, invoice.liters)
    self.goodsText:setText(string.format(getText("uwm_approve_goods"), UWM.getGoodName(ft), amount, UWMFrame.getRepeatText(invoice)))
    local pickupKey = UWMManager.getUsesDepot(ft) and UWMOrderDialog.getPickupPointKey(ft, invoice.isPallet) or "uwm_form_rowDirect"
    self.pickupText:setText(string.format(getText("uwm_approve_pickup"), getText(pickupKey)))
    self.priceText:setText(UWMFrame.getPriceText(ft, invoice.pricePer1000))
    self.totalLabel:setText(string.format(getText("uwm_approve_pays"), buyerName))

    -- an older request may already carry the buyer's discount: start from it
    self.discountInput:setText(invoice.discountPercent > 0 and UWMManager.formatPercent(invoice.discountPercent) or "")
    self:updateTotals()
    FocusManager:setFocus(self.discountInput)
end

-- nil = not a valid percent
function UWMApproveDialog:getDiscount()
    local text = self.discountInput:getText()
    if text == nil or text:match("^%s*$") then
        return 0
    end
    local percent = parseNumber(text)
    if percent == nil or percent < 0 or percent >= 100 then
        return nil
    end
    return percent
end

function UWMApproveDialog.getTotals(invoice, discount)
    if invoice.amountMode == UWMInvoice.AMOUNT.ALL then
        return nil
    end
    local full = invoice.liters * invoice.pricePer1000 / 1000
    local off = full * (discount or 0) / 100
    return full - off, full, off
end

function UWMApproveDialog:updateTotals()
    local UWM = PlayerTradingPlus
    local invoice = self.invoice
    local ft = invoice.fillTypeIndex
    local discount = self:getDiscount()
    local paid, full, off = UWMApproveDialog.getTotals(invoice, discount)
    local percentText = UWMManager.formatPercent(discount or 0)

    if full ~= nil then
        self.subtotalKey:setText(string.format(getText("uwm_approve_subtotal"), UWM.formatAmount(ft, invoice.liters),
            UWMFrame.getPriceText(ft, invoice.pricePer1000)))
        self.subtotalValue:setText(UWM.formatMoney(full))
    else
        self.subtotalKey:setText(getText("uwm_summary_amountAll"))
        self.subtotalValue:setText("")
    end
    if discount == nil then
        self.discountKey:setText(getText("uwm_error_badDiscount"))
        self.discountValue:setText("")
    elseif discount > 0 then
        self.discountKey:setText(string.format(getText("uwm_approve_discount"), percentText))
        self.discountValue:setText(off ~= nil and "- " .. UWM.formatMoney(off) or "")
    else
        self.discountKey:setText("")
        self.discountValue:setText("")
    end
    self.totalValue:setText(paid ~= nil and UWM.formatMoney(paid) or "-")
    self.noteText:setText((discount or 0) > 0 and string.format(getText("uwm_approve_note"),
        UWMManager.getFarmName(invoice.buyerFarmId), percentText) or "")
end

function UWMApproveDialog:onInputChanged()
    self:updateTotals()
end

function UWMApproveDialog:onClickApprove()
    local discount = self:getDiscount()
    if discount == nil then
        InfoDialog.show(getText("uwm_error_badDiscount"))
        return
    end
    local invoice = self.invoice
    self:close()
    UWMRequestEvent.sendRequest(UWMManager.ACTION.ACCEPT, {invoiceId = invoice.id, discountPercent = discount})
end

function UWMApproveDialog:onClickDecline()
    local invoice = self.invoice
    self:close()
    UWMRequestEvent.sendRequest(UWMManager.ACTION.DECLINE, {invoiceId = invoice.id})
end

function UWMApproveDialog:onClickBack()
    self:close()
end
