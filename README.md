# Specset — FedRAMP 20x Marketplace

Source repository for Specset's public FedRAMP information supporting our **Initial Implementation** listing on the [FedRAMP Marketplace](https://www.fedramp.gov/20x/).

**Canonical public endpoints (CDS-CSO-PUB):**

- Machine-readable: **https://specset.com/fedramp/fedramp.json** — served as `application/json`, no authentication, no approval workflow
- Human-readable: **https://specset.com/fedramp/**

`fedramp.json` conforms to the [FedRAMP Certification Package Overview JSON Schema (2026-06-24)](https://fedramp.gov/schemas/fedramp-certification-package-overview-schema-2026-06-24.json). The human-readable page is generated from `fedramp.json` by `build.py`, keeping the two formats consistent per [CDS-CSO-CBF](https://www.fedramp.gov/2026/reference/certification-data-sharing/#consistency-between-formats). Never hand-edit `index.html` — edit `fedramp.json`, run `python3 build.py`, and republish both files.

- **Provider:** Specset
- **Offering:** Specset Cloud Platform (SCP)
- **Website:** https://specset.com
- **Trust Center:** https://trust.specset.com (live; landing page public, no login)
- **Current stage:** Initial Implementation
- **Target framework:** FedRAMP 20x Class A
- **Federal use case:** Direct Use and Indirect Use — used directly by agency customers integrated into a federal information system, and/or included as a third-party information resource within other FedRAMP-certified cloud service offerings.

## Milestones toward FedRAMP Certification

Progress is measured against the goals below and updated at least quarterly, per the FedRAMP 2026 Consolidated Rules.

| Milestone | Target | Status |
|---|---|---|
| Initial Implementation marketplace listing requested | Jul 2026 | In progress |
| Public Trust Center / milestones page live at trust.specset.com | Jul 2026 | **Complete** |
| CDS-CSO-PUB public information published (JSON + human-readable) | Aug 2026 | In progress |
| Public service list with security categories (CDS-CSO-SVC) | Q3 2026 | In progress |
| Define minimum assessment scope / authorization boundary | Q3 2026 | Planned |
| Enter FedRAMP 20x Class A pipeline (opened Aug 3, 2026) | Aug 2026 | Planned |
| Baseline Key Security Indicators (KSI) evidence assembled | Q4 2026 | Planned |
| Independent assessment for a full operational class (B/C/D) **scheduled** | Within 24 months of listing (by Jul 2028) | Committed |

## References

- [CDS-CSO-PUB — Public Information](https://www.fedramp.gov/2026/reference/certification-data-sharing/#public-information)
- [CDS-CSO-SVC — Public Service List](https://www.fedramp.gov/2026/reference/certification-data-sharing/#public-service-list)
- [CDS-CSO-CBF — Consistency Between Formats](https://www.fedramp.gov/2026/reference/certification-data-sharing/#consistency-between-formats)
- [FedRAMP Marketplace Listing rules (2026 Consolidated Rules)](https://www.fedramp.gov/2026/providers/implement/marketplace/marketplace-listing/)
- [FedRAMP 20x](https://www.fedramp.gov/20x/)
