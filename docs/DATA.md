# DATA.md

All entries below reflect an independent live verification pass (2026-09-21) of every dataset the original plan cites — not the plan's own descriptions taken on faith.

## Datasets

| Dataset | Exists? | Real contents (verified) | License | Fit for stated use |
|---|---|---|---|---|
| IRDAI Handbook / Annual Report 2024-25 | CONFIRMED, public PDF | Company-wise and industry-wide incurred claims ratios, settlement data, premium figures | Public govt report | Good for calibration — see Regulatory section below |
| Kaggle: "Health insurance dataset — India-2022" (balajiadithya) | CONFIRMED | Excel, IRDAI-sourced, 2013–2022, multi-index tables. Confirmed content: Number of Policies, Number of Persons Covered, Gross Premium (Table 62) — insurer-level aggregate stats, **not** individual claims | Unclear — NOT stated on page, must verify before listing | **PARTIAL FIT — UNCONFIRMED.** The plan claims this file gives "TPA network hospital counts." This could not be confirmed from the public description. **Do not build a feature around this table until someone opens the actual Excel file and checks every sheet name.** See PROJECT_TRACK.md H0.4. |
| Kaggle: "India PMFBY statistics" (pyatakov) | CONFIRMED | District-wise enrollment, area insured, premiums, subsidies, crop-wise sums insured; scraped from the PMFBY dashboard as of Feb 2023 | **CC BY-NC-SA 4.0** — non-commercial, share-alike | Good fit for district panel, **but** the dataset author's own notes say state/district names are not synchronized between its two files, and some states are missing entirely. Budget a real hour for reconciliation (see PROJECT_TRACK.md H0.6) — this is a known last-hour blocker. |
| data.gov.in: PMFBY state/UT claims paid, 2019-20 to 2023-24 | CONFIRMED on OGD Platform | State/UT-level claims paid (₹ crore) by year — state-level only, no district breakdown | Government Open Data License | Matches the plan's description exactly. Note: several near-duplicate resources exist on data.gov.in with different year windows, some with "NA" for states like West Bengal/Gujarat/Jharkhand in some years — pick one resource, document its specific coverage gaps in an assumption ledger, do not silently zero-fill. |
| PIB PMFBY press notes | CONFIRMED | National-level PMFBY summary stats (56.96 crore applications, ₹1.54 lakh crore paid) | Public domain | Fine for a one-line deck stat, not a panel data source. |
| Kaggle: "Insurance Claims Dataset 2026 (FD & RA)" (mmumairkhattak) | CONFIRMED | 50,000 rows, 40 features, Fraud_Flag / Claim_Amount / Claim_Status targets, data dictionary + notebook included | **MIT — confirmed, no issue** | Good, low-risk independent sanity-check dataset. Not confirmed India-specific — keep the plan's own caveat about geography/feature mismatch. |
| Kaggle: "Insurance Fraud Detection" (arpan129) | CONFIRMED | Well-known ~15,000-row US auto-insurance fraud dataset (policy type, fault, address-change history fields) — not India-specific despite one description referencing IIM Calcutta | **Not clearly stated on page — check before including** | Usable only as a rough second sanity check, exactly as the plan frames it. Do not let its US-motor-claims schema influence feature engineering for the Indian synthetic core. |

**No dead or hallucinated links** — every dataset cited actually exists at the given URL.

**On "no India-specific claim-level fraud dataset exists":** CONFIRMED accurate. Academic work with India-specific fraud-labeled claim data (e.g. the Markov-model paper using 382,587 claims / 38,082 fraud labels) used private/proprietary data, not anything published. The synthetic-core justification in the plan is a genuine constraint, not a convenient excuse.

## Regulatory / calibration figures (verified against source)

| Figure | Plan's number | Verified figure | Verdict |
|---|---|---|---|
| Non-life incurred claims ratio, FY2024-25 | ~83% | **82.88%**, up from 82.52% the prior year | Accurate to within rounding |
| Claims settled by count, industry-wide | ~82% | Roughly consistent (one source: 82% by number vs. 71.3% by value for a related dataset) | Roughly consistent |
| TPA settlement share | ~72% | Could not be pinned to a specific line in the primary IRDAI report from search alone | Treat as "sourced via press coverage" per the plan's own labeling — do not cite as independently verified without opening the primary PDF |

**IRDAI Insurance Fraud Monitoring Framework Guidelines, 2025** — CONFIRMED real, issued 9 October 2025, **effective 1 April 2026**. As of this documentation's generation date, this framework has been in force for roughly six months. **Positioning note for the deck:** frame this as a regulation insurers are *currently* operating under, not an "upcoming" one. It replaces a 2013 circular, requires insurers to report fraud data to the IIB (Insurance Information Bureau) for a national cross-referencing database, and mandates board-level Fraud Monitoring Committees with FMR-1 annual reporting. ClaimLens Nexus's insight/ring-detection approach can legitimately be pitched as mirroring the kind of cross-entity pattern detection the IIB mandate is pushing insurers toward — a more specific and stronger pitch than a generic "AI for insurance" framing.

## Data audit — what's still open
- Confirm the balajiadithya TPA-hospital-count table actually exists (open the file)
- Lock licenses for balajiadithya and arpan129 datasets before packaging
- Reconcile PMFBY district-file state/district names against the synthetic core's state list
- Choose one data.gov.in PMFBY resource and document its specific year/state coverage gaps

## PENDING — cannot be documented without the original plan
Exact synthetic-data generator schema (fields, distributions, volumes) for policies/claims/hospitals/garages/agents. Tracked in PROJECT_TRACK.md.
