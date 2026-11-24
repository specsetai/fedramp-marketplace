#!/usr/bin/env python3
"""Copy the assessor's overall summary into fedramp.json (CPO-CSO-OSA).

The FedRAMP Recognized assessor supplies the overall summary of the Class C independent assessment
(IVV-IAS-OSA) as a JSON file of its own. This script copies the assessor's words from that file into
fedramp.json, under `overallSummaryOfAssessment`, without changing them, and records the SHA-256 of
the file it read, so anyone holding the supplied file can check the copy. Never edit the assessor's
text in fedramp.json by hand: re-run this script, then build.py.

The supplied file stays out of this repository, which is public. By default only the overall summary,
the assessment process statements and the status counts are copied; the recorded findings are
referenced, in the request-access trust-center edition that documentation[] names. With
`--findings public` the recorded findings are copied as well, so the public overview carries them.

    python3 assessment_summary.py SUMMARY.json                    # write; findings referenced
    python3 assessment_summary.py SUMMARY.json --findings public  # write; findings copied
    python3 assessment_summary.py SUMMARY.json --check            # fedramp.json carries the file's words
    python3 build.py
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
CPO = HERE / "fedramp.json"
KEY = "overallSummaryOfAssessment"

# The file the current section was copied from. A different file is refused until this is changed,
# so a new summary is a deliberate change reviewed in its own pull request.
EXPECTED_SHA256 = "6045607dd9c941e19e01c007c4f5c5551d91219b9b157834aa014f63c866becc"

# Specset's own words around the assessor's text. Everything else in the section is the assessor's.
INTRODUCTION = (
    "Prescient Security, LLC. (Assessor ID 202040) assessed the Specset Cloud Platform for FedRAMP 20x "
    "Class C. Under IVV-IAS-OSA it supplied the overall summary of its assessment on 2026-11-23. This "
    "section reproduces the summary without change, with the assessor's statements of its assessment "
    "process and sampling scope and the provider implementation status counts it reports (CPO-CSO-OSA). "
    "The assessor's findings for each practice are in the Class C Security Decision Record, which "
    "carries the assessment of all 203 practices as supplied (IVV-CSO-ICP)."
)
COUNTS_LABEL = "Provider implementation status, as assessed"
FINDINGS_REFERENCED = (
    "The assessor's overall summary as supplied, with its 51 recorded findings, each with the accepted "
    "current state and its limitations, is a restricted trust-center resource open to access requests, "
    "no NDA: \"Class C independent assessment: overall summary and recorded findings\" under "
    "documentation. The same findings are in the assessment of each practice in the Class C Security "
    "Decision Record."
)
FINDINGS_PUBLIC = (
    "The assessor's 51 recorded findings follow as supplied, each with the accepted current state and "
    "its limitations. Their source references are in the request-access edition, \"Class C independent "
    "assessment: overall summary and recorded findings\" under documentation, and in the Class C "
    "Security Decision Record."
)
FINDING_FIELDS = ("requirement_id", "title", "kind", "provider_implementation_status",
                  "assessor_free_text", "accepted_current_state", "limitations")


def section(src, raw, name, findings, cpo):
    if src["fedramp_id"] != cpo["serviceIdentification"]["fedRampPackageId"]:
        raise SystemExit(f"the summary is for {src['fedramp_id']}, not this offering")
    if not src["assessor_organization"] or not cpo["assessor"]["name"].startswith(src["assessor_organization"]):
        raise SystemExit(f"the summary is by {src['assessor_organization']}, not {cpo['assessor']['name']}")
    status = src["provider_implementation_status_source"]
    rec = src["recorded_findings"]
    out = {
        "rule": "CPO-CSO-OSA",
        "assessor": cpo["assessor"]["name"],
        "assessorID": cpo["assessor"]["assessorID"],
        "asOf": src["as_of"],
        "introduction": INTRODUCTION,
        "summary": list(src["overall_assessment_summary"]),
        "assessmentProcess": [
            {"requirement": p["source_requirement_id"], "statement": p["assessment_process_and_scope"]}
            for p in src["assessment_process"]
        ],
        "providerImplementationStatus": {
            "label": COUNTS_LABEL,
            "scope": {
                "keySecurityIndicators": src["provider_facing_scope"]["key_security_indicators"],
                "providerRules": src["provider_facing_scope"]["provider_rules"],
                "total": src["provider_facing_scope"]["total"],
            },
            "counts": dict(src["provider_implementation_status_counts"]),
            "ownership": src["provider_implementation_status_ownership"],
            "assessedRecordSha256": status["sha256"],
        },
        "recordedFindings": {
            "count": len(rec),
            "statement": FINDINGS_PUBLIC if findings == "public" else FINDINGS_REFERENCED,
        },
        "suppliedFile": {"name": name, "sha256": hashlib.sha256(raw).hexdigest()},
    }
    if sum(out["providerImplementationStatus"]["counts"].values()) != out["providerImplementationStatus"]["scope"]["total"]:
        raise SystemExit("the status counts do not add up to the assessed scope")
    if findings == "public":
        out["recordedFindings"]["findings"] = [{k: f[k] for k in FINDING_FIELDS} for f in rec]
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("summary", type=Path, help="the assessor's overall-summary JSON file, as supplied")
    ap.add_argument("--findings", choices=("referenced", "public"), default="referenced",
                    help="reference the recorded findings (default) or copy them into the public overview")
    ap.add_argument("--check", action="store_true",
                    help="fail if fedramp.json does not carry the file's words unchanged")
    a = ap.parse_args()

    raw = a.summary.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit(f"{a.summary.name} has SHA-256 {digest}, not the expected {EXPECTED_SHA256}")
    src = json.loads(raw)
    cpo = json.loads(CPO.read_text())

    if a.check:
        have = cpo.get(KEY)
        mode = "public" if have and "findings" in have.get("recordedFindings", {}) else "referenced"
        want = section(src, raw, a.summary.name, mode, cpo)
        if have != want:
            diff = sorted(k for k in set(want) | set(have or {}) if (have or {}).get(k) != want.get(k))
            print(f"{KEY} differs from {a.summary.name} in: {', '.join(diff)}; run without --check", file=sys.stderr)
            return 1
        print(f"{KEY} carries {a.summary.name} unchanged (findings {mode})")
        return 0

    new = {}
    for k, v in cpo.items():   # keep the section in a stable place: after the assessor
        if k == KEY:
            continue
        new[k] = v
        if k == "assessor":
            new[KEY] = section(src, raw, a.summary.name, a.findings, cpo)
    CPO.write_text(json.dumps(new, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote {KEY} to fedramp.json from {a.summary.name} (findings {a.findings}); now run build.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
