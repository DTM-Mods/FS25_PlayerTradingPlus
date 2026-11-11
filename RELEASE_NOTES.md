<p align="center">
  <img src="https://raw.githubusercontent.com/DTM-Mods/.github/main/assets/patch-notes.jpg" alt="Patch notes" width="100%">
</p>

# 0.12.1.0 — November 3, 2026

Renamed to **Player Trading+** (was Utilities & Waste Management). Zip `FS25_PlayerTradingPlus.zip`, new icon
(bolt, pallet of planks, growing corn), brand line "PT+ CO-OP", every page and text renamed. The old save file is
still read, so invoices and orders carry over; a depot placed under the old mod name has to be placed again.
0.12.1.0: the mod description in the mod list is up to date (bulk, pallets, standing orders, discount, goods
waiting in the depot).

# 0.11.0.0 — November 2, 2026

The seller can give a discount on standing sell orders. On a request the seller sets the discount in the new
Approve window; buyers can no longer set one.

# 0.10.0.0 — October 30, 2026

Standing Orders tab as cards in the CO-OP look; "Delete finished invoices" button in the footer.

# 0.9.0.0 — October 28, 2026

New CO-OP look for the page, the New window and the form. Goods put up for sale wait in the depot until
collected. Bulk goods (silo pipe) and pallet goods (pallet pad) can be traded. Discount on invoices.

# 0.7.0.0 / 0.8.0.0 — October 28, 2026

New CO-OP window and one-screen form (one item per invoice). Discount, Amount / Amount-in-liters swap, focus fix.

# 0.6.0.0 — October 26, 2026

The depot now includes the approved manure pit in front of the slurry tank. Its open end faces the same
direction as the office door, with manure pickup at that entrance. The UNIA silos/dryer and the marked
pallet pad beside the office are decorative for now; the pad does not spawn pallets.

The pit has building and tip collisions on all three walls. Placement and ground preparation cover the
new layout, and the shop picture shows the updated model. Export regenerates the depot's XML node mappings.

Standing offers also protect reserved stock during the production chain's automatic output processing.
The headless scenario for 1,000,000 charge stored and 500,000 offered sells only the other 500,000;
new surplus remains available and withdrawing the offer releases its unsold reservation.

Validation: 184 headless scenarios pass; Lua syntax, XML and localization checks pass; all 21 depot node
mappings resolve. The exported model was visually checked in GIANTS Editor. The relocated manure pickup,
placement and automatic production sale integration still require in-game testing.

Testing artifact: `FS25_UtilitiesWasteManagement.zip`, 13,072,296 bytes, 46 runtime files, each verified
against source. Source tools, tests and previews are excluded from the ZIP.

SHA-256: `72332267af80c7bd828bacdca6d403495403f67f9afe789d70426d323b004910`
