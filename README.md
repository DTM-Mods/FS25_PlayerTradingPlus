<p align="center">
  <a href="https://github.com/DTM-Mods"><img src="https://raw.githubusercontent.com/DTM-Mods/.github/main/assets/dtm-header.jpg" alt="DTM Mods by PropaineX & Fennell" width="100%"></a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/DTM-Mods/.github/main/assets/icons/FS25_PlayerTradingPlus.png" alt="Player Trading+ Pro Edition icon" width="128">
</p>

<h1 align="center">Player Trading+ Pro Edition</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Farming%20Simulator-25-2E6B4F" alt="Farming Simulator 25">
  <a href="https://github.com/DTM-Mods/FS25_PlayerTradingPlus/releases/latest"><img src="https://img.shields.io/github/v/release/DTM-Mods/FS25_PlayerTradingPlus?label=version&color=D9A441" alt="Latest version"></a>
  <img src="https://img.shields.io/badge/multiplayer-supported-2E6B4F" alt="Multiplayer supported">
  <a href="https://github.com/DTM-Mods"><img src="https://img.shields.io/badge/DTM-Mods-143326" alt="DTM Mods"></a>
</p>

<p align="center">
  <b>Farms buy and sell goods with each other through invoices and standing orders.</b><br>
  <sub>by PropaineX</sub>
</p>

<p align="center">
  <a href="https://github.com/DTM-Mods/FS25_PlayerTradingPlus/releases/latest"><img src="https://img.shields.io/badge/Download-latest%20release-D9A441?style=for-the-badge&logo=github&logoColor=143326&labelColor=E9C77A" alt="Download the latest release"></a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/DTM-Mods/.github/main/assets/features.jpg" alt="Features" width="100%">
</p>

Farming Simulator 25 mod by DTM Mods, PropaineX. Version 0.12.1.1, checked in game.
Renamed from "Utilities & Waste Management" in 0.12.0.0.

Farms buy and sell goods with each other through invoices and standing orders, in multiplayer or with several
farms in singleplayer. Money only moves between farms. Everything goes through the **Community Depot**.

## What you can trade
- **Electricity** goes straight from the seller's power-producing productions into the productions the buyer
  picks, and is paid for as it arrives.
- **Slurry and manure** are collected at the depot: slurry at the tank coupling, manure at the open end of the
  manure pit.
- **Bulk goods** (grain and everything else the game counts as bulk) come from the seller's silos and production
  outputs and are loaded at the depot's silo pipe.
- **Pallet goods** are sold by the liter. The seller's pallets are used up; the buyer gets new pallets (1,000 or
  5,000 l) on the depot's pallet pad.

<p align="center">
  <img src="https://raw.githubusercontent.com/DTM-Mods/.github/main/assets/how-it-works.jpg" alt="How it works" width="100%">
</p>

- **Player Trading+ page** in the ESC menu (also from the depot office door). It appears once a depot stands on
  the map. Tabs INCOMING / OUTGOING / STANDING ORDERS, summary cards, invoice cards with status pills.
- **New** opens the **PT+ CO-OP** window: *Invoice a farm*, *Request an invoice*, *Create a standing buy order*,
  *Create a standing sell order*. Then one form: farm, goods, price per 1,000 l (or kWh, the game's price as a
  guide), amount (a set amount or all in stock), discount and repeat (once, every day, every week).
  One item per invoice.
- **Only farm managers** send, accept, decline, withdraw or delete. Once paid, anyone on the buying farm can haul.
- **Goods wait in the depot.** Goods put up for sale leave the seller's storage and sit in the depot, still the
  seller's, until the buyer collects them. Unsold goods go back home (pallets come back on the pad).
- **Discounts:** the seller can give a discount on a bill or a standing sell order. On a request the seller sets
  it when approving. Both farms see the discount on the invoice, receipt and Details.
- **Standing orders** are open to every member: a sell order anyone can buy part or all of, a buy order anyone can
  fill. Money for a buy order is held when it is posted; withdrawing returns what's left.
- **Details** on every invoice: ordered, delivered / collected, refunded, discount, what the buyer paid and the
  seller got. Finished invoices can be deleted one by one or all at once.
- Payments show on the finance page as "Player trade sales" / "Player trade purchases".

## The Community Depot
Shop: Production > Selling points, $268,000, upkeep $268 a day. One per map unless the server admin allows more.
Every other farm is offered membership; members and the owner share the upkeep equally. Two months in debt =
suspended until paid. A member can leave but can't rejoin for 6 months. No depot (or no membership) = no trading.
The depot has a slurry tank, a manure pit, UNIA silos with a loading pipe for bulk goods, a pallet pad and an
office.

<!-- dtm-screenshots -->

<p align="center">
  <img src="https://raw.githubusercontent.com/DTM-Mods/.github/main/assets/screenshots.jpg" alt="Screenshots" width="100%">
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/DTM-Mods/.github/main/assets/screens/FS25_PlayerTradingPlus/shop.jpg" alt="The Community Depot" width="100%">
</p>

<!-- /dtm-screenshots -->

<p align="center">
  <img src="https://raw.githubusercontent.com/DTM-Mods/.github/main/assets/installation.jpg" alt="Installation" width="100%">
</p>

Download `FS25_PlayerTradingPlus.zip` from the [latest release](https://github.com/DTM-Mods/FS25_PlayerTradingPlus/releases/latest) and put it in `Documents/My Games/FarmingSimulator2025/mods`, without unzipping or renaming it. In multiplayer, the server and every player need the same version.

Saves from Utilities & Waste Management keep their invoices and orders, but the depot has to be placed again.

<p align="center">
  <img src="https://raw.githubusercontent.com/DTM-Mods/.github/main/assets/license.jpg" alt="License" width="100%">
</p>

MIT, see `LICENSE`.

<details>
<summary><b>For developers</b>: files, building and tests</summary>

### Building the zip yourself

Run `python tools/build_zip.py FS25_PlayerTradingPlus.zip` and put the zip in the FS25 `mods` folder.
Don't rename the zip. Saves from Utilities & Waste Management keep their invoices and orders, but the depot has to
be placed again.

### Files

- `modDesc.xml` - mod description and all texts
- `scripts/PlayerTradingPlus.lua` - startup, saving, join sync, notifications, finance rows
- `scripts/UWMInvoice.lua`, `scripts/UWMListing.lua` - one invoice / one standing order: fields, network, save
- `scripts/UWMManager.lua` - the trading and depot rules (server side)
- `scripts/UWMStock.lua` - a farm's storages, taking goods out, putting them back, electricity, reservations
- `scripts/UWMPallets.lua` - pallet goods: the seller's pallets, new pallets on the pad
- `scripts/UWMPickup.lua` - buyers collecting paid goods at the depot
- `scripts/UWMDepot.lua`, `placeables/depot/` - the depot placeable
- `scripts/UWMEvents.lua` - network events
- `scripts/gui/` + `gui/` - the ESC page (UWMFrame), CO-OP window (UWMCoopDialog), form (UWMOrderDialog),
  seller's approve window (UWMApproveDialog), dialog steps (UWMWizard), image sheet (UWMGui, `uwm_ui.dds`)
- `icon_PlayerTradingPlus.dds` - mod icon (`.png` = its source, drawn by `previews/icon_v7.py`)
- `tests/` - headless tests (Lua 5.1 via the Python package `lupa`), not part of the mod
- `tools/build_zip.py` - builds the mod zip from the shipped files
- `previews/` - mock-ups and the scripts that drew them; `source/` - depot model and texture sources
- `DESIGN.md` - the design and the rules it follows

### Tests

`python tests/run.py <folder with lupa> . tests` runs the trading scenarios; `python tests/check.py <folder with
lupa> .` checks Lua syntax, XML and that every text key exists.

</details>

---

<p align="center">
  <a href="https://github.com/DTM-Mods"><img src="https://raw.githubusercontent.com/DTM-Mods/.github/main/assets/dtm-intro.gif" alt="DTM Mods by PropaineX & Fennell" width="420"></a><br>
  <sub>Part of <a href="https://github.com/DTM-Mods">DTM Mods</a> (Designed To Manage) by PropaineX & Fennell</sub><br><br>
  <a href="https://ko-fi.com/dtmmods"><img src="https://img.shields.io/badge/Ko--fi-support%20DTM%20Mods-1F4D3A?logo=kofi&logoColor=F4F1E8" alt="Support DTM Mods on Ko-fi"></a>
  <a href="https://www.paypal.com/donate/?business=dtmmods%40gmail.com&amp;no_recurring=0&amp;item_name=DTM+Mods&amp;currency_code=USD"><img src="https://img.shields.io/badge/PayPal-donate-1F4D3A?logo=paypal&logoColor=F4F1E8" alt="Donate to DTM Mods with PayPal"></a><br>
  <a href="https://www.youtube.com/@DTMMods"><img src="https://img.shields.io/badge/YouTube-videos-1F4D3A?logo=youtube&logoColor=F4F1E8" alt="DTM Mods on YouTube"></a>
  <a href="https://dtmmods.itch.io"><img src="https://img.shields.io/badge/itch.io-our%20mods-1F4D3A?logo=itchdotio&logoColor=F4F1E8" alt="DTM Mods on itch.io"></a>
  <a href="https://www.kingmods.net/en/profile/dtmmods"><img src="https://img.shields.io/badge/KingMods-our%20mods-1F4D3A" alt="DTM Mods on KingMods"></a>
</p>
