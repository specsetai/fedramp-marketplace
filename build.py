#!/usr/bin/env python3
"""Generate the human-readable FedRAMP public information page from fedramp.json.

CDS-CSO-CBF (Consistency Between Formats) requires automation to keep the
human-readable and machine-readable formats consistent. This script is that
automation: fedramp.json is the single source of truth, and index.html is
generated from it. Never hand-edit index.html — edit fedramp.json and re-run:

    python3 build.py

Output: index.html (same directory), served alongside fedramp.json at
https://specset.com/fedramp/
"""
import json
import html
import re
from datetime import date, timezone, datetime
from pathlib import Path

HERE = Path(__file__).parent
data = json.loads((HERE / "fedramp.json").read_text())

si = data["serviceIdentification"]
sp = data["serviceProperties"]
contacts = {c["contactType"]: c for c in data["contactInformation"]}

def esc(v):
    return html.escape(str(v))

def contact_html(c):
    if not c:
        return na("Contact not published")
    parts = []
    if c.get("contactName"):
        parts.append(esc(c["contactName"]))
    if c.get("contactEmail"):
        parts.append(f'<a href="mailto:{esc(c["contactEmail"])}">{esc(c["contactEmail"])}</a>')
    if c.get("contactPhone"):
        parts.append(esc(c["contactPhone"]))
    return " · ".join(parts)

def na(reason):
    return f'<span class="na">Not applicable — {esc(reason)}</span>'

def link(url, label=None):
    return f'<a href="{esc(url)}">{esc(label or url)}</a>'

# --- The 16 CDS-CSO-PUB fields, each rendered from the JSON (or an explicit
# --- not-applicable statement so reviewers can see every field was evaluated).
tc = sp.get("trustCenter")
if tc:
    tc_html = link(tc["url"]) + "<br><em>Access instructions:</em> " + esc(tc.get("accessRequestInstructions", "No authentication required."))
else:
    tc_html = na("no trust center published")

scg = sp.get("secureConfigurationGuidance")
assessor = data.get("assessor")
services = data.get("certifiedServices")

if services:
    svc_rows = "".join(
        f"<tr><td>{esc(s['serviceName'])}</td><td>{esc(s['serviceDescription'])}</td><td>{esc(s['dateAvailable'])}</td></tr>"
        for s in services
    )
    svc_html = f'<table class="inner"><thead><tr><th>Service</th><th>Description</th><th>Available since</th></tr></thead><tbody>{svc_rows}</tbody></table>'
else:
    svc_html = ('<span class="pending">In development — the detailed service list and per-service security '
                'categories are being finalized alongside our Minimum Assessment Scope definition and will be '
                'published here (CDS-CSO-SVC).</span>')

tp = data.get("thirdPartyInformationResources")
if tp:
    cert = tp.get("certified", []); nonc = tp.get("nonCertified", [])
    cert_rows = "".join(
        f'<tr><td><a href="https://www.fedramp.gov/marketplace/products/{esc(r["fedRampCertifiedThirdPartyInformationResource"])}/">{esc(r["fedRampCertifiedThirdPartyInformationResource"])}</a></td><td>{esc(r["useCase"])}</td></tr>'
        for r in cert)
    nonc_rows = "".join(
        f'<tr><td>{esc(r["name"])}<br><small>{esc(r["provider"])}</small></td><td>{esc(r["useCase"])}</td></tr>'
        for r in nonc)
    tp_html = (f'<p><strong>FedRAMP Certified ({len(cert)})</strong></p><table class="inner"><thead><tr><th>FedRAMP ID</th><th>Use</th></tr></thead><tbody>{cert_rows}</tbody></table>'
               f'<p><strong>Not FedRAMP Certified ({len(nonc)})</strong></p><table class="inner"><thead><tr><th>Resource</th><th>Use</th></tr></thead><tbody>{nonc_rows}</tbody></table>')
else:
    tp_html = na("no third-party information resources declared")


docs = data.get("documentation")
if docs:
    doc_rows = "".join(
        f"<tr><td>{esc(x['name'])}</td><td>{esc(x['type'])}</td><td>{esc(x['summary'])}</td><td>{esc(x['availability'])}</td></tr>"
        for x in docs)
    doc_html = f'<table class="inner"><thead><tr><th>Document</th><th>Type</th><th>Summary</th><th>Availability</th></tr></thead><tbody>{doc_rows}</tbody></table>'
else:
    doc_html = '<span class="pending">In development — an overview of provider-supplied documentation (name, type, summary, availability) will be published here.</span>'

meta = data.get("metadata")
if meta:
    ao = meta.get("accountableOfficial", {})
    meta_html = (f'<table><tbody>'
                 f'<tr><th>Accountable official</th><td>{esc(ao.get("name", ""))}, {esc(ao.get("title", ""))} · <a href="mailto:{esc(ao.get("email", ""))}">{esc(ao.get("email", ""))}</a></td></tr>'
                 f'<tr><th>Version</th><td>{esc(meta.get("version", ""))}</td></tr>'
                 f'<tr><th>Last updated</th><td>{esc(meta.get("lastUpdated", ""))}</td></tr>'
                 f'<tr><th>Source of update</th><td>{esc(meta.get("updateSource", ""))}</td></tr>'
                 f'</tbody></table>')
else:
    meta_html = ""

FIELDS = [
    ("FedRAMP ID",
     esc(si["fedRampPackageId"]) + (
         f'<br><a href="https://www.fedramp.gov/marketplace/products/{esc(si["fedRampPackageId"])}/">FedRAMP Marketplace listing</a>'
         if re.match(r"^FR\d{10}", si["fedRampPackageId"])
         else '<br><em>No FedRAMP ID has been assigned yet; the provider name and service acronym are used as the package identifier per FedRAMP schema guidance.</em>')),
    ("Service Model", esc(", ".join(sp["serviceType"]))),
    ("Deployment Model", esc(sp["deploymentModel"])),
    ("Business Category", esc(", ".join(sp.get("businessCategory", []))) or na("not categorized")),
    ("UEI Number", esc(si.get("ueiNumber")) if si.get("ueiNumber") else na("no UEI registered")),
    ("Sales Contact Information", contact_html(contacts.get("Sales"))),
    ("Security Contact Information", contact_html(contacts.get("Security"))),
    ("Product Website", link(si["website"])),
    ("Product Logo", link(si["logo"])),
    ("Overall Service Description", esc(si["serviceDescription"])),
    ("Services and Security Categories", svc_html),
    ("Secure Configuration Guidance",
     link(scg["url"]) if scg else '<span class="pending">In development — secure configuration guidance is being authored and will be linked here.</span>'),
    ("Documentation Overview", doc_html),
    ("Trust Center", tc_html),
    ("Next Ongoing Certification Report Date",
     esc(sp["nextOngoingCertificationReportDate"]) if sp.get("nextOngoingCertificationReportDate")
     else na("Specset is at the Initial Implementation stage and does not yet hold a FedRAMP certification, so no Ongoing Certification Report is scheduled")),
    ("Third-Party Information Resources",
     tp_html),
    ("FedRAMP Recognized Independent Assessor",
     f'{esc(assessor["name"])} (Assessor ID {esc(assessor["assessorID"])})' if assessor
     else na("an independent assessor has not yet been engaged; per MKT-IIP-DLA an independent assessment will be scheduled within 24 months of initial listing")),
]

rows = "".join(f"<tr><th>{esc(name)}</th><td>{value}</td></tr>" for name, value in FIELDS)
today = datetime.now(timezone.utc).date().isoformat()

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{esc(si['providerName'])} — FedRAMP Public Information ({esc(si['serviceName'])})</title>
<meta name="description" content="FedRAMP CDS-CSO-PUB public information for {esc(si['serviceName'])}, in human-readable and machine-readable formats." />
<style>
  :root {{ color-scheme: light dark; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; max-width: 880px; margin: 0 auto; padding: 2.5rem 1.25rem; }}
  h1 {{ font-size: 1.9rem; margin-bottom: .25rem; }}
  .sub {{ color: #667085; margin-top: 0; }}
  .machine {{ background: #f2f4f7; border: 1px solid #e4e7ec; border-radius: 8px; padding: .75rem 1rem; margin: 1.25rem 0; }}
  @media (prefers-color-scheme: dark) {{ .machine {{ background: #1d2430; border-color: #333; }} th, td {{ border-color: #333 !important; }} }}
  table {{ width: 100%; border-collapse: collapse; margin: 1rem 0 2rem; }}
  th, td {{ text-align: left; padding: .6rem .5rem; border-bottom: 1px solid #e4e7ec; vertical-align: top; }}
  th {{ width: 34%; font-weight: 600; }}
  table.inner th {{ width: auto; font-size: .8rem; text-transform: uppercase; letter-spacing: .04em; color: #667085; }}
  .na {{ color: #667085; }}
  .pending {{ color: #93370d; }}
  footer {{ color: #667085; font-size: .85rem; margin-top: 2.5rem; border-top: 1px solid #e4e7ec; padding-top: 1rem; }}
  a {{ color: #1570ef; }}
</style>
</head>
<body>
  <h1>{esc(si['providerName'])} — FedRAMP Public Information</h1>
  <p class="sub">{esc(si['serviceName'])} ({esc(si['serviceAcronym'])}) · FedRAMP {esc(si['certificationType'])} · Initial Implementation · last generated {today}</p>

  <div class="machine">
    <strong>Machine-readable format:</strong> <a href="https://specset.com/fedramp/fedramp.json">https://specset.com/fedramp/fedramp.json</a><br>
    Conforms to the <a href="https://fedramp.gov/schemas/fedramp-certification-package-overview-schema-2026-06-24.json">FedRAMP Certification Package Overview schema (2026-06-24)</a>.
    Served as <code>application/json</code> with no authentication, approval workflow, or access justification required.
  </div>

  <p>This page publishes the information required by FedRAMP
  <a href="https://www.fedramp.gov/2026/reference/certification-data-sharing/#public-information">CDS-CSO-PUB (Public Information)</a>.
  Every enumerated field is listed below; fields that do not yet apply to Specset's current stage are stated explicitly rather than omitted.</p>

  <table>
    <tbody>{rows}</tbody>
  </table>

  <h2>Package metadata (CPO-CSO-MTD)</h2>
  {meta_html}

  <footer>
    This page is generated automatically from <a href="https://specset.com/fedramp/fedramp.json">fedramp.json</a>
    to keep human-readable and machine-readable formats consistent
    (<a href="https://www.fedramp.gov/2026/reference/certification-data-sharing/#consistency-between-formats">CDS-CSO-CBF</a>).
    Source: <a href="https://github.com/specsetai/fedramp-marketplace">github.com/specsetai/fedramp-marketplace</a> ·
    Contact: <a href="mailto:security@specset.com">security@specset.com</a>
  </footer>
</body>
</html>
"""

(HERE / "index.html").write_text(page)
print(f"Wrote index.html ({len(page)} bytes) from fedramp.json")
