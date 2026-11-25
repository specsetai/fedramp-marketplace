#!/usr/bin/env python3
"""Copy the assessor's overall summary into fedramp.json (CPO-CSO-OSA).

The FedRAMP Recognized assessor supplies the overall summary of the Class C independent assessment
(IVV-IAS-OSA) in two files: a public summary, whose paragraphs go in the public overview, and the
complete controlled annex, which carries the same paragraphs with the findings for every practice and
is open only to necessary parties. This script copies the assessor's words from the public summary
into fedramp.json, under `overallSummaryOfAssessment`, without changing them, and records the SHA-256
of the file it read, so anyone holding the supplied file can check the copy. Never edit the
assessor's text in fedramp.json by hand: re-run this script, then build.py.

Neither file is committed: this repository is public, and the controlled annex is not. The section
names the annex and its SHA-256, as the public summary gives them; the annex itself is a
request-access trust-center resource that documentation[] names. `--annex` reads the annex only to
confirm it is the file the summary names and carries the same paragraphs; nothing is copied from it.

    python3 assessment_summary.py SUMMARY.json                 # write
    python3 assessment_summary.py SUMMARY.json --check         # fedramp.json carries the file's words
    python3 assessment_summary.py SUMMARY.json --check --annex ANNEX.json   # and ANNEX is the named annex
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

# The file the current section was copied from: Prescient Security's public assessment summary of
# 2026-11-24 (Specset-Public-Assessment-Summary-2026-11-24.json). A different file is refused until
# this is changed, so a new summary is a deliberate change reviewed in its own pull request.
EXPECTED_SHA256 = "bc5dc788bd33d33dfe97181aa370a0e260a800fc9bec18e3fd2c8650430c6a8c"

ANNEX_TITLE = "Class C independent assessment: complete controlled annex (all 203 findings)"

# Specset's own words around the assessor's text. Everything else in the section is the assessor's.
INTRODUCTION = (
    "Prescient Security, LLC. (Assessor ID 202040) assessed the Specset Cloud Platform for FedRAMP 20x "
    "Class C. Under IVV-IAS-OSA it supplied the overall summary of its assessment for this overview, in "
    "its public edition of 2026-11-24. This section reproduces the summary's paragraphs and the "
    "assessor's statement of the assessment dates without change (CPO-CSO-OSA). The assessor's findings "
    "for each of the 203 practices are in its complete controlled annex, open to necessary parties as "
    "described below; the Class C Security Decision Record carries its assessment of each practice as "
    "supplied (IVV-CSO-ICP)."
)
ANNEX_STATEMENT = (
    "The assessor's complete controlled annex carries the same summary with its findings for all 203 "
    "practices (46 Key Security Indicators and 157 provider rules), each with the accepted current state, "
    "its limitations and its source references. It is not public. Necessary parties obtain it, as the "
    f"assessor supplied it, as a restricted trust-center resource open to access requests, no NDA: \"{ANNEX_TITLE}\" "
    "under documentation, following the trust center's access instructions in this document."
)


def section(src, raw, name, cpo):
    if src["fedramp_id"] != cpo["serviceIdentification"]["fedRampPackageId"]:
        raise SystemExit(f"the summary is for {src['fedramp_id']}, not this offering")
    if not src["assessor_organization"] or not cpo["assessor"]["name"].startswith(src["assessor_organization"]):
        raise SystemExit(f"the summary is by {src['assessor_organization']}, not {cpo['assessor']['name']}")
    annex = src["controlled_annex"]
    return {
        "rule": "CPO-CSO-OSA",
        "assessor": cpo["assessor"]["name"],
        "assessorID": cpo["assessor"]["assessorID"],
        "edition": src["edition"],
        "introduction": INTRODUCTION,
        "summary": list(src["overall_assessment_summary"]),
        "assessmentDates": {
            "originalAssessmentCompleted": src["original_assessment_completion_date"],
            "extendedReviewCompleted": src["assessment_completion_date"],
            "rulesRelease": src["rules_reference"],
            "basis": src["assessment_date_basis"],
        },
        "controlledAnnex": {
            "title": ANNEX_TITLE,
            "name": annex["delivery_filename"],
            "sha256": annex["sha256"],
            "statement": ANNEX_STATEMENT,
        },
        "suppliedFile": {"name": name, "sha256": hashlib.sha256(raw).hexdigest()},
    }


def check_annex(path, src):
    """The annex is the file the summary names, with the same paragraphs. Nothing is copied from it."""
    raw = path.read_bytes()
    want = src["controlled_annex"]["sha256"]
    if hashlib.sha256(raw).hexdigest() != want:
        raise SystemExit(f"{path.name} is not the controlled annex the summary names (SHA-256 {want})")
    if json.loads(raw)["overall_assessment_summary"] != src["overall_assessment_summary"]:
        raise SystemExit(f"{path.name} carries different summary paragraphs from the public summary")
    print(f"{path.name} is the controlled annex the summary names, with the same paragraphs")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("summary", type=Path, help="the assessor's public assessment-summary JSON file, as supplied")
    ap.add_argument("--check", action="store_true",
                    help="fail if fedramp.json does not carry the file's words unchanged")
    ap.add_argument("--annex", type=Path,
                    help="the controlled annex as supplied: confirm it is the file the summary names")
    a = ap.parse_args()

    raw = a.summary.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit(f"{a.summary.name} has SHA-256 {digest}, not the expected {EXPECTED_SHA256}")
    src = json.loads(raw)
    cpo = json.loads(CPO.read_text())
    if a.annex:
        check_annex(a.annex, src)

    if a.check:
        have = cpo.get(KEY)
        want = section(src, raw, a.summary.name, cpo)
        if have != want:
            diff = sorted(k for k in set(want) | set(have or {}) if (have or {}).get(k) != want.get(k))
            print(f"{KEY} differs from {a.summary.name} in: {', '.join(diff)}; run without --check", file=sys.stderr)
            return 1
        print(f"{KEY} carries {a.summary.name} unchanged")
        return 0

    new = {}
    for k, v in cpo.items():   # keep the section in a stable place: after the assessor
        if k == KEY:
            continue
        new[k] = v
        if k == "assessor":
            new[KEY] = section(src, raw, a.summary.name, cpo)
    CPO.write_text(json.dumps(new, indent=2, ensure_ascii=False) + "\n")
    print(f"Wrote {KEY} to fedramp.json from {a.summary.name}; now run build.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
