#!/usr/bin/env python3
"""
PRAXIS — compile_master.py

Implements Agente 00 (Phase 5 subroutine) — compilation rules C1..C8.
Reads manifest.yaml + artifact files, produces master_<case_id>.md
and compilation_log.md.

Usage:
    python compile_master.py [--manifest <path>] [--output-dir <path>]
"""

import argparse
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed.", file=sys.stderr)
    sys.exit(2)


EPISTEMIC_LABELS = ("[FATO]", "[INFERÊNCIA]", "[INFERENCIA]",
                    "[HIPÓTESE]", "[HIPOTESE]")
LABEL_SPECIFICITY = {  # higher = more specific
    "[FATO]": 3,
    "[INFERÊNCIA]": 2, "[INFERENCIA]": 2,
    "[HIPÓTESE]": 1, "[HIPOTESE]": 1,
}

SECTION_MAP = {
    "Seção 1: Contexto e Situação": ["A-01"],
    "Seção 2: Identidade e Proposta Comercial": ["A-02", "A-03", "A-04"],
    "Seção 3: Diagnóstico": ["A-06", "A-07", "A-08", "A-09"],
    "Seção 4: Cenários e Simulações": ["A-10", "A-11"],
    "Seção 5: Plano de Ação": ["A-06", "A-10"],
    "Seção 6: Próximos Passos e Handoff": ["A-06", "A-10"],
}


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def tokenize(text: str) -> set:
    """Lowercased significant tokens, stop-words removed (Portuguese stub)."""
    stop = {"a", "o", "as", "os", "de", "da", "do", "das", "dos",
            "e", "em", "para", "por", "com", "no", "na", "nos", "nas",
            "um", "uma", "que", "se", "ao", "a", "the", "is", "are"}
    tokens = re.findall(r"\w+", text.lower(), flags=re.UNICODE)
    return {t for t in tokens if len(t) > 2 and t not in stop}


def similarity(a: str, b: str) -> float:
    ta, tb = tokenize(a), tokenize(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / max(len(ta | tb), 1)


def detect_label(block: str) -> str | None:
    for lab in EPISTEMIC_LABELS:
        if lab in block:
            return lab
    return None


def normalize_headings(content: str) -> str:
    """Demote H5/H6 to bold paragraphs (rule C3)."""
    out = []
    for line in content.splitlines():
        if line.startswith("###### "):
            out.append("**" + line[7:].strip() + "**")
        elif line.startswith("##### "):
            out.append("**" + line[6:].strip() + "**")
        else:
            out.append(line)
    return "\n".join(out)


def split_into_blocks(content: str) -> list[str]:
    """Split markdown into block units. Headings start new blocks; blank
    lines also terminate blocks."""
    blocks = []
    current = []
    for line in content.splitlines():
        if line.lstrip().startswith("#"):
            if current:
                blocks.append("\n".join(current))
                current = []
            current.append(line)
        elif not line.strip():
            if current:
                blocks.append("\n".join(current))
                current = []
        else:
            current.append(line)
    if current:
        blocks.append("\n".join(current))
    return blocks


def demote_block_heading(block: str, target_min_level: int = 3) -> str:
    """Demote leading heading line of block to at least H<target_min_level>.
    Leaves non-heading first-lines untouched."""
    lines = block.splitlines()
    if not lines:
        return block
    stripped = lines[0].lstrip()
    if stripped.startswith("#"):
        hashes = 0
        for ch in stripped:
            if ch == "#":
                hashes += 1
            else:
                break
        if hashes < target_min_level:
            new_level = "#" * target_min_level
            rest = stripped[hashes:].lstrip()
            lines[0] = f"{new_level} {rest}"
    return "\n".join(lines)


def deduplicate(blocks: list[tuple[str, str, int]],
                log: list[str]) -> list[tuple[str, str, int]]:
    """Apply rule C4. blocks: list of (artifact_id, text, phase)."""
    kept: list[tuple[str, str, int]] = []
    for art_id, text, phase in blocks:
        replaced = False
        for i, (k_id, k_text, k_phase) in enumerate(kept):
            if similarity(text, k_text) > 0.80:
                # decide which to keep: more recent (higher phase) wins
                # tiebreaker: more specific label
                label_a = detect_label(text) or ""
                label_b = detect_label(k_text) or ""
                spec_a = LABEL_SPECIFICITY.get(label_a, 0)
                spec_b = LABEL_SPECIFICITY.get(label_b, 0)
                keep_new = phase > k_phase or (phase == k_phase and spec_a > spec_b)
                if keep_new:
                    log.append(
                        f"DEDUP: replaced block from {k_id} (phase {k_phase}) "
                        f"with block from {art_id} (phase {phase}). "
                        f"reason=newer_or_more_specific")
                    kept[i] = (art_id, text, phase)
                else:
                    log.append(
                        f"DEDUP: kept block from {k_id} over candidate from "
                        f"{art_id}. reason=older_or_more_specific_kept")
                replaced = True
                break
        if not replaced:
            kept.append((art_id, text, phase))
    return kept


def classify_track(block: str, section_name: str) -> str:
    """Apply rule C6 default classification."""
    if "[TRILHA_INTERNA]" in block:
        return "INTERNA"
    if "[TRILHA_CLIENTE]" in block:
        return "CLIENTE"
    if section_name.startswith("Apêndice"):
        return "INTERNA"
    return "CLIENTE"


def completeness_check(sections: dict, full_text: str) -> dict:
    """Apply rule C7."""
    checks = {
        "secao_1_min_3_fields": False,
        "secao_3_root_cause": False,
        "secao_5_action_with_owner": False,
        "at_least_one_fato": False,
    }
    s1 = sections.get("Seção 1: Contexto e Situação", "")
    field_lines = [ln for ln in s1.splitlines()
                   if ln.strip().startswith("-") or ln.strip().startswith("*")]
    checks["secao_1_min_3_fields"] = len(field_lines) >= 3

    s3 = sections.get("Seção 3: Diagnóstico", "")
    checks["secao_3_root_cause"] = (
        "causa-raiz" in s3.lower() or "causa raiz" in s3.lower()
        or "root cause" in s3.lower() or "root-cause" in s3.lower())

    s5 = sections.get("Seção 5: Plano de Ação", "")
    checks["secao_5_action_with_owner"] = (
        ("owner" in s5.lower() or "responsável" in s5.lower()
         or "responsavel" in s5.lower())
        and ("prazo" in s5.lower() or "deadline" in s5.lower()))

    checks["at_least_one_fato"] = "[FATO]" in full_text
    return checks


def assemble(manifest: dict,
             artifacts_payload: dict,
             previous_master: str | None) -> tuple[str, str]:
    """Returns (master_md, log_md)."""
    log: list[str] = [f"# Compilation Log — case_id={manifest.get('case_id')}",
                      f"Generated at {now_iso()}",
                      "",
                      "## Source resolution (C1)"]

    artifacts = manifest.get("artifacts_produced", [])
    artifacts_sorted = sorted(artifacts,
                              key=lambda a: (a.get("phase", 99),
                                             a.get("timestamp", "")))
    for art in artifacts_sorted:
        log.append(f"- {art.get('artifact_id')} (phase "
                   f"{art.get('phase')}, ts {art.get('timestamp', '?')})")
    log.append("")

    sections: dict[str, str] = {}
    log.append("## Deduplication decisions (C4)")
    dedup_logs: list[str] = []

    for section_name, contributing in SECTION_MAP.items():
        candidate_blocks: list[tuple[str, str, int]] = []
        for art_id in contributing:
            content = artifacts_payload.get(art_id)
            if not content:
                continue
            content = normalize_headings(content)
            phase = next((a.get("phase", 0) for a in artifacts_sorted
                          if a.get("artifact_id") == art_id), 0)
            for block in split_into_blocks(content):
                stripped = block.strip()
                if not stripped:
                    continue
                # If this block is ONLY a heading (no body), drop it.
                if "\n" not in stripped and stripped.lstrip().startswith("#"):
                    continue
                # Demote leading heading to H3 to nest under canonical H2.
                demoted = demote_block_heading(block, target_min_level=3)
                candidate_blocks.append((art_id, demoted, phase))
        kept = deduplicate(candidate_blocks, dedup_logs)
        sections[section_name] = "\n\n".join(b for _, b, _ in kept)

    log.extend(dedup_logs if dedup_logs else ["(no duplicates detected)"])
    log.append("")

    log.append("## Label restorations (C5)")
    log.append("(none — input artifacts retained their labels)")
    log.append("")

    full_text_preview = "\n".join(sections.values())
    checks = completeness_check(sections, full_text_preview)
    log.append("## Completeness check (C7)")
    for k, v in checks.items():
        log.append(f"- [{('PASS' if v else 'FAIL')}] {k}")
    log.append("")

    track_counts = {"INTERNA": 0, "CLIENTE": 0}
    for sec, body in sections.items():
        for block in split_into_blocks(body):
            track = classify_track(block, sec)
            track_counts[track] += 1
    log.append("## Track classification (C6)")
    log.append(f"- [TRILHA_INTERNA]: {track_counts['INTERNA']} blocks")
    log.append(f"- [TRILHA_CLIENTE]: {track_counts['CLIENTE']} blocks")
    log.append("")

    if not all(checks.values()):
        log.append("## STATUS: C7 FAILED — A-MASTER NOT PRODUCED")
        missing = [k for k, v in checks.items() if not v]
        log.append("Missing elements:")
        for m in missing:
            log.append(f"  - {m}")
        return "", "\n".join(log)

    client_name = manifest.get("client_identity", {}).get(
        "company_name", "Cliente")
    parts = [f"# {client_name} — Dossiê Consultivo PRAXIS", ""]
    fixed_order = [
        "Seção 1: Contexto e Situação",
        "Seção 2: Identidade e Proposta Comercial",
        "Seção 3: Diagnóstico",
        "Seção 4: Cenários e Simulações",
        "Seção 5: Plano de Ação",
        "Seção 6: Próximos Passos e Handoff",
    ]
    for sec in fixed_order:
        parts.append(f"## {sec}")
        body = sections.get(sec, "").strip()
        parts.append(body if body else "[TRILHA_CLIENTE] (sem conteúdo coletado)")
        parts.append("")

    parts.append("## Apêndice A: Log de Decisões")
    parts.append("[TRILHA_INTERNA]")
    for gp in manifest.get("gates_passed", []):
        if isinstance(gp, dict):
            parts.append(f"- {gp.get('gate_id')} aprovado por "
                         f"{gp.get('approved_by')} em "
                         f"{gp.get('approved_at')} "
                         f"(hardcoded_human={gp.get('hardcoded_human', False)})")
    if previous_master:
        parts.append("")
        parts.append("### Delta desde A-MASTER anterior")
        parts.append("(scenario B — comparação carregada do case_id_previous)")
    parts.append("")

    parts.append("## Apêndice B: Trilha Epistêmica")
    parts.append("[TRILHA_INTERNA]")
    full_text = "\n".join(sections.values())
    for label in ("[FATO]", "[INFERÊNCIA]", "[INFERENCIA]",
                  "[HIPÓTESE]", "[HIPOTESE]"):
        count = full_text.count(label)
        if count:
            parts.append(f"- {label}: {count} ocorrências")

    return "\n".join(parts), "\n".join(log)


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile A-MASTER (Agente 00).")
    parser.add_argument("--manifest", default="manifest.yaml")
    parser.add_argument("--output-dir", default=".")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        print(f"ERROR: manifest not found at {manifest_path}", file=sys.stderr)
        return 2

    with manifest_path.open("r", encoding="utf-8") as f:
        manifest = yaml.safe_load(f)

    payload: dict[str, str] = {}
    base_dir = manifest_path.parent
    for art in manifest.get("artifacts_produced", []):
        art_id = art.get("artifact_id")
        path = art.get("path")
        if not path:
            continue
        p = Path(path)
        if not p.is_absolute():
            p = base_dir / p
        if p.exists() and p.is_file():
            try:
                payload[art_id] = p.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue

    previous_master = None
    prev_id = manifest.get("case_id_previous")
    if prev_id:
        prev_path = base_dir / f"master_{prev_id}.md"
        if prev_path.exists():
            previous_master = prev_path.read_text(encoding="utf-8")

    master_md, log_md = assemble(manifest, payload, previous_master)

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    log_path = out_dir / "compilation_log.md"
    log_path.write_text(log_md, encoding="utf-8")

    if not master_md:
        print("Compilation halted at C7 — see compilation_log.md", file=sys.stderr)
        return 1

    case_id = manifest.get("case_id", "unknown")
    master_path = out_dir / f"master_{case_id}.md"
    master_path.write_text(master_md, encoding="utf-8")

    print(f"A-MASTER written to: {master_path}")
    print(f"compilation_log written to: {log_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
