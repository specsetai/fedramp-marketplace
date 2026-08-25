# Specset — FedRAMP 20x Marketplace

Source repository for Specset's public FedRAMP information supporting our **Initial Implementation** listing on the [FedRAMP Marketplace](https://www.fedramp.gov/20x/).

**Canonical public endpoints (CDS-CSO-PUB):**

- Machine-readable: **https://specset.com/fedramp/fedramp.json** — served as `application/json`, no authentication, no approval workflow
- Human-readable: **https://specset.com/fedramp/**

`fedramp.json` conforms to the [FedRAMP Certification Package Overview JSON Schema (2026-06-24)](https://fedramp.gov/schemas/fedramp-certification-package-overview-schema-2026-06-24.json). The human-readable page is generated from `fedramp.json` by `build.py`, keeping the two formats consistent per [CDS-CSO-CBF](https://www.fedramp.gov/2026/reference/certification-data-sharing/#consistency-between-formats). Never hand-edit `index.html` — edit `fedramp.json`, run `python3 build.py`, and republish both files.

- **Provider:** Specset
- **Offering:** Specset Cloud Platform (SCP)
- **FedRAMP Package ID:** **FR2631258135** — [Marketplace listing](https://www.fedramp.gov/marketplace/products/FR2631258135/) (Initial Implementation since 2026-08-13)
- **Website:** https://specset.com
- **Trust Center:** https://trust.specset.com (live; landing page public, no login)
- **Current stage:** Initial Implementation
- **Target framework:** FedRAMP 20x Class A (pipeline open since 2026-08-03)
- **Federal use case:** Direct Use and Indirect Use — used directly by agency customers integrated into a federal information system, and/or included as a third-party information resource within other FedRAMP-certified cloud service offerings.

## Milestones toward FedRAMP Certification

Progress is measured against the goals below and updated at least quarterly, per the FedRAMP 2026 Consolidated Rules.

| Milestone | Target | Status |
|---|---|---|
| Initial Implementation marketplace listing | Jul 2026 | **Complete** — FR2631258135, listed 2026-08-13 |
| Public Trust Center / milestones page live at trust.specset.com | Jul 2026 | **Complete** |
| CDS-CSO-PUB public information published (JSON + human-readable) | Aug 2026 | **Complete** — this repository, served at specset.com/fedramp/ |
| Public service list (CDS-CSO-SVC) and third-party information resources (MAS-CSO-TPR) published | Aug 2026 | **Complete** — `certifiedServices` / `thirdPartyInformationResources` in `fedramp.json` |
| Define minimum assessment scope / authorization boundary (MAS-CSO-IIR) | Q3 2026 | **Complete** — GCP project `specset-prod-assured` (Assured Workloads, us-west1) plus the third-party resources listed |
| Certification Package (CPO, Security Decision Record, example Ongoing Certification Report) assembled and self-verified | Sep 2026 | In progress |
| SOC 2 Type II report (Class A basis, FRC-CLA-ASF) issued | Sep 2026 | In progress — audit period Apr 15 – Jul 15, 2026 |
| FedRAMP 20x Class A application submitted | Sep 2026 | Planned |
| Baseline Key Security Indicators (KSI) evidence assembled | Q4 2026 | In progress — persistent validation (drift detection, vulnerability detection, alerting) running since 2026-08-22 |
| Independent assessment for a full operational class (B/C/D) **scheduled** | Within 24 months of listing (by Jul 2028) | Committed |

## Updating the listing

FedRAMP reads this listing from `fedramp.json` (it mirrors the JSON verbatim into the Marketplace record). To change anything shown on the Marketplace:

1. Edit `fedramp.json` (never `index.html`), run `python3 build.py`, open a PR — CI validates the JSON against the FedRAMP schema and checks `index.html` is regenerated.
2. Merge, then republish **both** `fedramp.json` and `index.html` to `https://specset.com/fedramp/` (the marketing site hosts copies; the URLs above are the canonical endpoints FedRAMP polls).
3. Submit the **[For CSPs] Marketplace Listing Request Form** — https://help.fedramp.gov/hc/en-us/requests/new?ticket_form_id=50939227168027 — choosing **"an update to an existing listing"**, citing Package ID **FR2631258135**, and stating that the JSON at `https://specset.com/fedramp/fedramp.json` has been updated. FedRAMP does not accept listing changes by email. Per the form's guidance, CSPs onboarded via JSON update the JSON directly; the form tells FedRAMP to re-pull it.
4. Update the milestone table above at least quarterly (MKT-IIP-DCP).

Before applying for Class A certification, `fedRampPackageId` must carry the assigned FedRAMP ID (it does: FR2631258135), and the package must be self-verified within 7 days of submitting the **[For CSPs] FedRAMP 20x Certification Application Form (Class A)** — https://help.fedramp.gov/hc/en-us/requests/new?ticket_form_id=51137131584283.

## References

- [CDS-CSO-PUB — Public Information](https://www.fedramp.gov/2026/reference/certification-data-sharing/#public-information)
- [CDS-CSO-SVC — Public Service List](https://www.fedramp.gov/2026/reference/certification-data-sharing/#public-service-list)
- [CDS-CSO-CBF — Consistency Between Formats](https://www.fedramp.gov/2026/reference/certification-data-sharing/#consistency-between-formats)
- [FedRAMP Marketplace Listing rules (2026 Consolidated Rules)](https://www.fedramp.gov/2026/providers/implement/marketplace/marketplace-listing/)
- [FedRAMP 20x](https://www.fedramp.gov/20x/)
