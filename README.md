# Specset — FedRAMP 20x Marketplace

Source repository for Specset's public FedRAMP information supporting our **Initial Implementation** listing on the [FedRAMP Marketplace](https://www.fedramp.gov/20x/).

**Canonical public endpoints (CDS-CSO-PUB):**

- Machine-readable: **https://specset.com/fedramp/fedramp.json** — served as `application/json`, no authentication, no approval workflow
- Human-readable: **https://specset.com/fedramp/**

`fedramp.json` conforms to the [FedRAMP Certification Package Overview JSON Schema (2026-06-24)](https://fedramp.gov/schemas/fedramp-certification-package-overview-schema-2026-06-24.json). The human-readable page is generated from `fedramp.json` by `build.py`, keeping the two formats consistent per [CDS-CSO-CBF](https://www.fedramp.gov/2026/reference/certification-data-sharing/#consistency-between-formats). Never hand-edit `index.html` — edit `fedramp.json`, run `python3 build.py`, and republish both files.

- **Provider:** Specset
- **Offering:** Specset Cloud Platform (SCP)
- **FedRAMP Package ID:** **FR2631258135** — [Marketplace listing](https://www.fedramp.gov/marketplace/products/FR2631258135/) (Initial Implementation since 2026-08-13). This is the sole active listing for the offering; a duplicate created at intake, FR2631747321, is pending retirement, requested 2026-08-31 and again in listing-update ticket #67448 (2026-09-14).
- **Website:** https://specset.com
- **Trust Center:** https://trust.specset.com (live; landing page public, no login)
- **Current stage:** Initial Implementation
- **Target framework:** FedRAMP 20x Class A (pipeline open since 2026-08-03; application filed 2026-09-14, help.fedramp.gov #67451, under FedRAMP review — nothing is certified yet), then Class C on the same boundary
- **Federal use case:** Direct Use (MKT-IIP-AGU) — agency staff will use the platform directly. The evidence of intent: a federal agency evaluation tenant provisioned with CUI mode enabled since 2026-09-13, the agency's confirmation of the Direct Use case on 2026-08-24, and a paid pilot pending procurement through one of the agency's contractors. No agency has used the service in production yet; the tenant will be listed in the Ongoing Certification Report when agency use begins. Contractor tenants are the contractor's own information systems; a contractor holding a federal contract may invite agency personnel as members of its tenant, and contractors handling CUI under their own contracts may request CUI mode. Specset is not included as a third-party information resource in another cloud service offering, so the Indirect Use case does not apply.
- **Security contact / FedRAMP Security Inbox:** fedramp@specset.com

## Milestones toward FedRAMP Certification

Progress is measured against the goals below and updated at least quarterly, per the FedRAMP 2026 Consolidated Rules.

| Milestone | Target | Status |
|---|---|---|
| Initial Implementation marketplace listing | Jul 2026 | **Complete** — FR2631258135, listed 2026-08-13 |
| Public Trust Center / milestones page live at trust.specset.com | Jul 2026 | **Complete** |
| CDS-CSO-PUB public information published (JSON + human-readable) | Aug 2026 | **Complete** — this repository, served at specset.com/fedramp/. Version 2026.09.14 (commit 18be5d37) is the one filed with the Class A application; the live JSON and page were verified byte-identical to this repository, and the JSON valid against the FedRAMP schema, on 2026-09-14 |
| Public service list and third-party information resources (MAS-CSO-TPR) published | Aug 2026 | **Complete** — `certifiedServices` / `thirdPartyInformationResources` in `fedramp.json`. Per-service security categories are published with the detailed service list at the 2026-12-01 report |
| Define minimum assessment scope / authorization boundary (MAS-CSO-IIR) | Q3 2026 | **Complete** — GCP project `specset-prod-assured` (Assured Workloads, us-west1) plus the third-party resources listed |
| SOC 2 Type II report (Class A basis, FRC-CLA-ASF) issued | Sep 2026 | **Complete** — Prescient Assurance LLC, issued 2026-08-31, Security TSC, period 2026-04-15 to 2026-07-15, unqualified, no exceptions; published on the Trust Center as a restricted, view-only resource with no NDA gate |
| Certification Package (CPO, Security Decision Record, example Ongoing Certification Report, information-resources inventory, procedures, twelve supporting-evidence documents) assembled | Sep 2026 | **Complete** — Security Decision Record v2026.09.14.5 filed with the application; the package is published on the Trust Center as restricted resources (22 requestable, no NDA) since 2026-09-14, and was self-verified the same day (FRC-APP-FCP) |
| FedRAMP 20x Class A application submitted | Sep 2026 | **Complete** — filed 2026-09-14 (help.fedramp.gov #67451); listing update requested the same day (#67448: refresh from this JSON, Direct Use only, retire FR2631747321) |
| FedRAMP 20x Class A certification decision | Oct 2026 | In review — FedRAMP's stated goal is a decision within 30 days of the application; during review the package changes only for corrections and reviewer requests |
| First Ongoing Certification Report published | 2026-12-01 | Scheduled — date published in `fedramp.json` (`nextOngoingCertificationReportDate`) |
| Baseline Key Security Indicators (KSI) evidence assembled | Q4 2026 | In progress — persistent validation (drift detection, vulnerability detection, alerting) running since 2026-08-22 |
| Independent assessment for a full operational class (B/C/D) **scheduled** | Within 24 months of listing (by Aug 2028) | In progress — assessor engaged for a Class C certification assessment (Prescient Security, LLC; statement of work issued 2026-07-15 and signed by Specset 2026-07-30); assessment dates not set. Class A itself requires no independent assessment (FRC-CLA-IVV is optional) |

## Updating the listing

FedRAMP reads this listing from `fedramp.json` (it mirrors the JSON verbatim into the Marketplace record). To change anything shown on the Marketplace:

1. Edit `fedramp.json` (never `index.html`), run `python3 build.py`, open a PR — CI validates the JSON against the FedRAMP schema and checks `index.html` is regenerated.
2. Merge, then republish **both** `fedramp.json` and `index.html` to `https://specset.com/fedramp/` (the marketing site hosts copies; the URLs above are the canonical endpoints FedRAMP polls). Confirm the published files match the merged commit byte for byte and record the republish date. The Security Decision Record cites these URLs as the evidence for CDS-CSO-PUB, CDS-CSO-CBF, MAS-CSO-TPR, CCM-OCR-NRD, FRC-CSO-POP and AFC-CSO-INB, so a stale copy makes six rule statements describe a document that is not the one published. The live copy was verified byte-identical to version 2026.09.14 on 2026-09-14, the day the Class A application was filed.

   ```sh
   curl -s https://specset.com/fedramp/fedramp.json | diff - fedramp.json && echo "JSON matches"
   curl -s https://specset.com/fedramp/ | diff - index.html && echo "page matches"
   ```
3. Submit the **[For CSPs] Marketplace Listing Request Form** — https://help.fedramp.gov/hc/en-us/requests/new?ticket_form_id=50939227168027 — choosing **"an update to an existing listing"**, citing Package ID **FR2631258135**, and stating that the JSON at `https://specset.com/fedramp/fedramp.json` has been updated. FedRAMP does not accept listing changes by email. Per the form's guidance, CSPs onboarded via JSON update the JSON directly; the form tells FedRAMP to re-pull it.
4. Update the milestone table above at least quarterly (MKT-IIP-DCP).

The Class A application was filed on 2026-09-14 through the **[For CSPs] FedRAMP 20x Certification Application Form** — https://help.fedramp.gov/hc/en-us/requests/new?ticket_form_id=51137131584283 — as ticket #67451, after the FRC-APP-FCP self-verification that day (the byte check in step 2 included). While the application is under review, change `fedramp.json` only for corrections and reviewer requests, run the step 2 byte check after each republish, and note the change on ticket #67451. The same seven-day self-verification applies before any later application (Class C).

## References

- [CDS-CSO-PUB — Public Information](https://www.fedramp.gov/2026/reference/certification-data-sharing/#public-information)
- [CDS-CSO-CBF — Consistency Between Formats](https://www.fedramp.gov/2026/reference/certification-data-sharing/#consistency-between-formats)
- [FRC-APP-FCP — Fresh FedRAMP Certification Package](https://www.fedramp.gov/2026/reference/fedramp-certification/#fresh-fedramp-certification-package)
- [FedRAMP Marketplace Listing rules (2026 Consolidated Rules)](https://www.fedramp.gov/2026/providers/implement/marketplace/marketplace-listing/)
- [FedRAMP 20x](https://www.fedramp.gov/20x/)
