#!/usr/bin/env python3
"""
PRAXIS — advance_phase.py

Update the case manifest after a gate is approved.

Usage:
    python advance_phase.py --gate G0..G6 --approved-by <consultant_id>
                            [--manifest <path>] [--reason <text>]
                            [--auto-confirm]   (only honored for AUTO gates)

HARDCODED HUMAN GATES: G2, G5, G6.
For these gates the script ALWAYS prompts for literal "yes" on stdin.
The --auto-confirm flag is REJECTED for hardcoded human gates.
"""

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed.", file=sys.stderr)
    sys.exit(2)


HARDCODED_HUMAN_GATES = {"G2", "G5", "G6"}
GATE_TO_NEXT_PHASE = {"G0": 2, "G1": 3, "G2": 3, "G3": 4, "G4": 6, "G5": 6}
ALL_GATES = ["G0", "G1", "G2", "G3", "G4", "G5", "G6"]


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def confirm_human_gate(gate_id: str) -> bool:
    """Require literal 'yes' on stdin for hardcoded human gates."""
    print(f"Gate {gate_id} requer revisao humana — HARDCODED HUMAN.")
    print("Confirme a aprovacao digitando 'yes' (qualquer outra resposta cancela).")
    try:
        response = input("> ").strip().lower()
    except EOFError:
        return False
    return response == "yes"


def main() -> int:
    parser = argparse.ArgumentParser(description="Advance case after a gate approval.")
    parser.add_argument("--gate", required=True, choices=ALL_GATES)
    parser.add_argument("--approved-by", required=True,
                        help="Consultant ID approving the gate")
    parser.add_argument("--manifest", default="manifest.yaml",
                        help="Path to manifest.yaml")
    parser.add_argument("--reason", default="",
                        help="Optional reason / notes for this gate")
    parser.add_argument("--auto-confirm", action="store_true",
                        help="Auto-confirm AUTO gates without stdin prompt. "
                             "REJECTED for hardcoded human gates.")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    if not manifest_path.exists():
        print(f"ERROR: manifest not found at {manifest_path}", file=sys.stderr)
        return 2

    with manifest_path.open("r", encoding="utf-8") as f:
        manifest = yaml.safe_load(f)

    gate_id = args.gate

    # Hardcoded human enforcement.
    if gate_id in HARDCODED_HUMAN_GATES:
        if args.auto_confirm:
            print(f"ERROR: Gate {gate_id} is HARDCODED HUMAN — "
                  f"--auto-confirm is rejected.", file=sys.stderr)
            return 3
        if not confirm_human_gate(gate_id):
            print(f"Gate {gate_id} NOT approved. Phase remains active.")
            return 1

    # Already passed?
    if gate_id in manifest.get("gates_passed", []):
        # gates_passed is stored as list of dicts in v1.0; tolerate both shapes.
        passed_ids = []
        for item in manifest.get("gates_passed", []):
            if isinstance(item, dict):
                passed_ids.append(item.get("gate_id"))
            else:
                passed_ids.append(item)
        if gate_id in passed_ids:
            print(f"Gate {gate_id} already approved previously.")
            return 0

    # Record approval.
    record = {
        "gate_id": gate_id,
        "approved_by": args.approved_by,
        "approved_at": now_iso(),
        "hardcoded_human": gate_id in HARDCODED_HUMAN_GATES,
        "reason": args.reason,
    }
    manifest.setdefault("gates_passed", []).append(record)

    # Remove from pending.
    pending = manifest.get("gates_pending", [])
    manifest["gates_pending"] = [g for g in pending if g != gate_id]

    # Update phase if applicable.
    if gate_id in GATE_TO_NEXT_PHASE:
        old_phase = manifest.get("current_phase", 1)
        new_phase = GATE_TO_NEXT_PHASE[gate_id]
        if new_phase > old_phase:
            manifest["current_phase"] = new_phase
            manifest.setdefault("phase_history", []).append({
                "phase": old_phase,
                "exited_at": now_iso(),
                "transition_gate": gate_id,
            })

    manifest["updated_at"] = now_iso()

    with manifest_path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(manifest, f, sort_keys=False, allow_unicode=True)

    print(f"Gate {gate_id} aprovado por {args.approved_by} em {record['approved_at']}.")
    print(f"Fase atual: {manifest['current_phase']}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
