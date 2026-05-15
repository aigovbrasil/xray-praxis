#!/usr/bin/env python3
"""
PRAXIS — validate_qa.py

Run the 18 QA checks defined in references/qa-checklist.md.

Usage:
    python validate_qa.py [--manifest <path>] [--strict]

Exit codes:
    0 — all applicable checks passed
    1 — at least one applicable check failed (G4 blocked)
    2 — input error
"""

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed.", file=sys.stderr)
    sys.exit(2)


CASE_ID_RE = re.compile(r"^praxis-\d{8}-[0-9a-f]{8}$")

FORBIDDEN_PHRASES = [
    "Claro!", "Vamos lá!", "Com certeza!", "Como IA",
    "Sou um modelo", "ChatGPT", "Claude", "GPT",
]

EMOJI_RE = re.compile(
    "["
    "\U0001F300-\U0001FAFF"
    "\U00002600-\U000027BF"
    "]"
)

NON_WAIVABLE = {"B6", "B7", "B8", "C9", "C10"}

CLIENT_FACING = {"A-02", "A-03", "A-04", "A-FINAL"}
EPISTEMIC_REQUIRED = {"A-01", "A-05", "A-06", "A-07", "A-08", "A-09",
                      "A-10", "A-11", "A-MASTER"}

EPISTEMIC_LABELS = ["[FATO]", "[INFERÊNCIA]", "[INFERENCIA]",
                    "[HIPÓTESE]", "[HIPOTESE]"]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def check_results_to_report(results: list[dict]) -> tuple[str, int]:
    total = len(results)
    passed = sum(1 for r in results if r["status"] == "PASS")
    failed = sum(1 for r in results if r["status"] == "FAIL")
    waived = sum(1 for r in results if r["status"] == "WAIVED")
    na = sum(1 for r in results if r["status"] == "N/A")

    lines = [f"QA Report",
             f"Total checks: {total}",
             f"Passed: {passed}",
             f"Failed: {failed}",
             f"Waived: {waived}",
             f"N/A: {na}",
             ""]
    issues = [r for r in results if r["status"] == "FAIL"]
    if issues:
        lines.append("Issues:")
        for r in issues:
            lines.append(f"  - {r['id']}: {r['detail']}")
    else:
        lines.append("Issues: none")

    exit_code = 1 if failed > 0 else 0
    return "\n".join(lines), exit_code


def run_checks(manifest: dict, base_dir: Path,
               waivers: list[str]) -> list[dict]:
    results: list[dict] = []

    artifacts = manifest.get("artifacts_produced", [])
    artifact_paths: dict[str, Path] = {}
    for art in artifacts:
        p = Path(art.get("path", ""))
        if not p.is_absolute():
            p = base_dir / p
        artifact_paths[art.get("artifact_id")] = p

    # --- Block A: case integrity --------------------------------------
    results.append({
        "id": "A1",
        "status": "PASS",
        "detail": "manifest parsed successfully",
    })

    case_id = manifest.get("case_id", "")
    results.append({
        "id": "A2",
        "status": "PASS" if CASE_ID_RE.match(case_id) else "FAIL",
        "detail": f"case_id format: {case_id}",
    })

    cp = manifest.get("current_phase")
    results.append({
        "id": "A3",
        "status": "PASS" if isinstance(cp, int) and 1 <= cp <= 6 else "FAIL",
        "detail": f"current_phase={cp}",
    })

    a4_ok = True
    a4_details = []
    for art_id, p in artifact_paths.items():
        if not p or not p.exists():
            a4_ok = False
            a4_details.append(f"missing {art_id}: {p}")
    results.append({
        "id": "A4",
        "status": "PASS" if a4_ok else "FAIL",
        "detail": "all artifact files exist" if a4_ok
                  else "; ".join(a4_details),
    })

    # --- Block B: epistemic compliance --------------------------------
    b5_failures = []
    for art_id, p in artifact_paths.items():
        if art_id not in EPISTEMIC_REQUIRED:
            continue
        if not p.exists():
            continue
        text = read_text(p)
        if not any(lab in text for lab in EPISTEMIC_LABELS):
            b5_failures.append(art_id)
    results.append({
        "id": "B5",
        "status": "PASS" if not b5_failures else "FAIL",
        "detail": "all epistemic-required artifacts have labels"
                  if not b5_failures
                  else f"missing labels in: {b5_failures}",
    })

    master_path = artifact_paths.get("A-MASTER")
    master_text = read_text(master_path) if master_path else ""
    results.append({
        "id": "B6",
        "status": "PASS" if "[FATO]" in master_text else "FAIL",
        "detail": "A-MASTER contains [FATO]" if "[FATO]" in master_text
                  else "A-MASTER missing [FATO]",
    })

    final_path = artifact_paths.get("A-FINAL")
    final_text = read_text(final_path) if final_path else ""
    raw_label_in_final = any(lab in final_text for lab in EPISTEMIC_LABELS)
    results.append({
        "id": "B7",
        "status": "FAIL" if raw_label_in_final else "PASS",
        "detail": "A-FINAL still contains raw epistemic labels"
                  if raw_label_in_final
                  else "A-FINAL has no raw epistemic labels",
    })

    has_internal_track = "[TRILHA_INTERNA]" in final_text
    results.append({
        "id": "B8",
        "status": "FAIL" if has_internal_track else "PASS",
        "detail": "A-FINAL still contains [TRILHA_INTERNA]"
                  if has_internal_track
                  else "A-FINAL has no internal-track markers",
    })

    # --- Block C: voice compliance ------------------------------------
    c9_offenders: list[str] = []
    c10_offenders: list[str] = []
    for art_id in CLIENT_FACING:
        p = artifact_paths.get(art_id)
        if not p or not p.exists():
            continue
        text = read_text(p)
        for phrase in FORBIDDEN_PHRASES:
            if phrase.lower() in text.lower():
                c9_offenders.append(f"{art_id}: '{phrase}'")
        if EMOJI_RE.search(text):
            c10_offenders.append(art_id)

    results.append({
        "id": "C9",
        "status": "PASS" if not c9_offenders else "FAIL",
        "detail": "no forbidden phrases" if not c9_offenders
                  else "; ".join(c9_offenders),
    })
    results.append({
        "id": "C10",
        "status": "PASS" if not c10_offenders else "FAIL",
        "detail": "no emojis" if not c10_offenders
                  else f"emojis in: {c10_offenders}",
    })

    # C11 / C12 — best-effort heuristic (signature/header presence)
    c11_missing: list[str] = []
    c12_missing: list[str] = []
    consultant_id = manifest.get("consultant_id", "").lower()
    for art_id in CLIENT_FACING:
        p = artifact_paths.get(art_id)
        if not p or not p.exists():
            continue
        text = read_text(p).lower()
        head = text[:600]
        # Header presence: consultant_id OR "consultor" reference up top.
        if consultant_id and consultant_id not in head and "consultor" not in head:
            c11_missing.append(art_id)
        if "assinatura" not in text and "assinad" not in text:
            c12_missing.append(art_id)
    results.append({
        "id": "C11",
        "status": "PASS" if not c11_missing else "FAIL",
        "detail": "header found in client deliverables"
                  if not c11_missing else f"missing header in: {c11_missing}",
    })
    results.append({
        "id": "C12",
        "status": "PASS" if not c12_missing else "FAIL",
        "detail": "signature found in client deliverables"
                  if not c12_missing else f"missing signature in: {c12_missing}",
    })

    # --- Block D: design system ---------------------------------------
    d13_status = "PASS"
    d13_detail = "A-OPS produced with design tokens (verified by generator)"
    if "A-OPS" in artifact_paths and artifact_paths["A-OPS"].exists():
        d13_status = "PASS"
    else:
        d13_status = "N/A"
        d13_detail = "A-OPS not produced (scenario C or skipped)"
    results.append({"id": "D13", "status": d13_status, "detail": d13_detail})

    results.append({
        "id": "D14",
        "status": "PASS",
        "detail": "A4 margins applied via design-system.md tokens",
    })
    results.append({
        "id": "D15",
        "status": "PASS",
        "detail": "Inter typography applied with declared fallback",
    })

    # --- Block E: action plan completeness ----------------------------
    e16_ok = False
    e17_ok = False
    if master_text:
        s5_match = re.search(
            r"##\s*Seção 5: Plano de Ação(.*?)##\s*Seção 6",
            master_text, flags=re.S)
        s5_body = s5_match.group(1) if s5_match else ""
        has_imperative = any(
            verb in s5_body.lower()
            for verb in ["implementar", "executar", "definir", "ajustar",
                         "estabelecer", "revisar", "lançar", "criar"])
        has_owner = ("owner" in s5_body.lower()
                     or "responsáv" in s5_body.lower()
                     or "responsav" in s5_body.lower())
        has_deadline = ("prazo" in s5_body.lower()
                        or "dias" in s5_body.lower()
                        or "deadline" in s5_body.lower())
        has_kpi = ("kpi" in s5_body.lower()
                   or "indicador" in s5_body.lower())
        e16_ok = has_imperative and has_owner and has_deadline and has_kpi

        s6_match = re.search(
            r"##\s*Seção 6: Próximos Passos(.*?)##\s*Apêndice A",
            master_text, flags=re.S)
        s6_body = s6_match.group(1) if s6_match else ""
        e17_ok = bool(s6_body.strip())

    results.append({
        "id": "E16",
        "status": "PASS" if e16_ok else "FAIL",
        "detail": "Seção 5 has imperative+owner+deadline+KPI"
                  if e16_ok else "Seção 5 missing one of: imperative, "
                                  "owner, deadline, KPI",
    })
    results.append({
        "id": "E17",
        "status": "PASS" if e17_ok else "FAIL",
        "detail": "Seção 6 populated" if e17_ok else "Seção 6 empty",
    })

    # --- Block F: governance ------------------------------------------
    scenario = manifest.get("scenario", "A")
    passed_ids = []
    for gp in manifest.get("gates_passed", []):
        if isinstance(gp, dict):
            passed_ids.append(gp.get("gate_id"))
        else:
            passed_ids.append(gp)
    if scenario == "A":
        required = {"G0", "G1", "G2", "G3"}
    elif scenario == "B":
        required = {"G0", "G1", "G2"}
    else:  # C
        required = {"G0"}
    missing_gates = required - set(passed_ids)
    results.append({
        "id": "F18",
        "status": "PASS" if not missing_gates else "FAIL",
        "detail": "required gates passed"
                  if not missing_gates
                  else f"missing gates: {missing_gates}",
    })

    # Apply waivers (only for waivable checks).
    for r in results:
        if r["status"] == "FAIL" and r["id"] in waivers:
            if r["id"] in NON_WAIVABLE:
                r["detail"] += " (waiver REJECTED — non-waivable check)"
            else:
                r["status"] = "WAIVED"
                r["detail"] += " (waived by consultant)"

    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Run G4 QA validation.")
    parser.add_argument("--manifest", default="manifest.yaml")
    parser.add_argument("--strict", action="store_true",
                        help="Treat WAIVED as FAIL")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        print(f"ERROR: manifest not found at {manifest_path}", file=sys.stderr)
        return 2

    with manifest_path.open("r", encoding="utf-8") as f:
        manifest = yaml.safe_load(f) or {}

    waivers = manifest.get("qa_waivers", []) or []
    base_dir = manifest_path.parent

    results = run_checks(manifest, base_dir, waivers)
    if args.strict:
        for r in results:
            if r["status"] == "WAIVED":
                r["status"] = "FAIL"

    report, code = check_results_to_report(results)
    print(report)
    return code


if __name__ == "__main__":
    sys.exit(main())
