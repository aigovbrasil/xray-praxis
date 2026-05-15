#!/usr/bin/env python3
"""
PRAXIS — init_case.py

Create a new case manifest.yaml.

Usage:
    python init_case.py --consultant <id> --client <name> [--briefing <path>]
                        [--scenario A|B|C] [--output-dir <path>]
"""

import argparse
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed. Run: pip install pyyaml --break-system-packages",
          file=sys.stderr)
    sys.exit(2)


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def make_case_id() -> str:
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    short_uuid = uuid.uuid4().hex[:8]
    return f"praxis-{today}-{short_uuid}"


def build_manifest(consultant: str,
                   client: str,
                   briefing: str | None,
                   scenario: str) -> dict:
    return {
        "case_id": make_case_id(),
        "consultant_id": consultant,
        "scenario": scenario,
        "client_identity": {
            "company_name": client,
            "segment": "",
            "cnpj": "",
            "city": "",
            "state": "",
            "employees": None,
            "annual_revenue_brl": None,
            "decision_makers": [],
            "drive_references": [],
        },
        "current_phase": 1,
        "phase_history": [],
        "artifacts_produced": [],
        "gates_passed": [],
        "gates_pending": ["G0", "G1", "G2", "G3", "G4", "G5", "G6"],
        "case_id_previous": None,
        "briefing_path": briefing,
        "created_at": now_iso(),
        "updated_at": now_iso(),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize a new PRAXIS case.")
    parser.add_argument("--consultant", required=True, help="Consultant identifier")
    parser.add_argument("--client", required=True, help="Client company name")
    parser.add_argument("--briefing", default=None,
                        help="Path to briefing file (optional)")
    parser.add_argument("--scenario", default="A", choices=["A", "B", "C"],
                        help="Scenario A (full), B (review), C (fast proposal)")
    parser.add_argument("--output-dir", default=".",
                        help="Directory in which to write manifest.yaml")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    manifest = build_manifest(
        consultant=args.consultant,
        client=args.client,
        briefing=args.briefing,
        scenario=args.scenario,
    )

    manifest_path = output_dir / "manifest.yaml"
    with manifest_path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(manifest, f, sort_keys=False, allow_unicode=True)

    print(f"Case initialized: {manifest['case_id']}")
    print(f"Manifest written to: {manifest_path}")
    print(f"Scenario: {args.scenario}")
    print(f"Current phase: 1")
    return 0


if __name__ == "__main__":
    sys.exit(main())
