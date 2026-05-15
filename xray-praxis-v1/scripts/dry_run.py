#!/usr/bin/env python3
"""
PRAXIS — dry_run.py

End-to-end synthetic exercise of all six phases. Used as the
functional acceptance test for the build.

Steps:
1.  Create temp directory.
2.  Initialize manifest with synthetic consultant + client.
3.  Phase 1: normalize fake briefing, print labeled claims.
4.  Phase 2: generate fake commercial proposal skeleton.
5.  Phase 3: apply 5 Whys to fake problem.
6.  Phase 4: generate one scenario table.
7.  Phase 5: compile all fake artifacts into master doc.
8.  Phase 6: produce placeholder final deliverable.
9.  Run validate_qa.py against the placeholder.
10. Print PASS if all phases executed without error; FAIL with details.
"""

import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: pyyaml not installed.", file=sys.stderr)
    sys.exit(2)


SCRIPT_DIR = Path(__file__).resolve().parent
PRAXIS_DIR = SCRIPT_DIR.parent


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def write(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def step_init(workdir: Path) -> Path:
    print("[1/10] Init case via init_case.py")
    cmd = [sys.executable, str(SCRIPT_DIR / "init_case.py"),
           "--consultant", "consultor.teste",
           "--client", "Empresa Sintetica Ltda",
           "--scenario", "A",
           "--output-dir", str(workdir)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"init_case failed: {r.stderr}")
    return workdir / "manifest.yaml"


def add_artifact(manifest_path: Path, art_id: str, phase: int, rel_path: str):
    with manifest_path.open("r", encoding="utf-8") as f:
        m = yaml.safe_load(f)
    m.setdefault("artifacts_produced", []).append({
        "artifact_id": art_id,
        "phase": phase,
        "path": rel_path,
        "timestamp": now_iso(),
    })
    m["updated_at"] = now_iso()
    with manifest_path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(m, f, sort_keys=False, allow_unicode=True)


def step_phase1(workdir: Path, manifest_path: Path):
    print("[2/10] Phase 1 — synthetic A-01")
    a01 = """# Normalized Follow Up — Empresa Sintetica Ltda

## Identidade do cliente
- [FATO] Empresa atua em servicos de manutencao predial.
- [FATO] Faturamento anual declarado: R$ 4,2 mi.
- [INFERÊNCIA] Margem operacional provavel em torno de 9%.
- [HIPÓTESE] Possivel concentracao de receita em 3 clientes-chave.

## Problema primario
[FATO] Queda de 18% na margem nos ultimos 6 meses, declarada pelo socio.

## Stakeholders
- Socio fundador (decisao final)
- Gerente operacional (executor)

## Cenario roteado
A — Diagnostico Completo.
"""
    p = workdir / "A-01.md"
    write(p, a01)
    add_artifact(manifest_path, "A-01", 1, "A-01.md")


def step_phase2(workdir: Path, manifest_path: Path):
    print("[3/10] Phase 2 — synthetic A-02")
    a02 = """# Proposta Comercial — Empresa Sintetica Ltda

Consultor: consultor.teste
Data: 2025-04-25
Validade: 30 dias

## 1. Contextualizacao
A empresa registra queda de margem nos ultimos 6 meses e busca diagnostico.

## 2. Metodologia
Engajamento estruturado em 6 etapas, distribuido em 3 sessoes.

## 3. Entregaveis
- Diagnostico executivo
- Plano de acao 5W2H
- Planilha operacional
- Sessao de handoff

## 4. Investimento
[PLACEHOLDER]

## 5. Cronograma
- Semana 1-2: imersao e diagnostico
- Semana 3: simulacao e plano
- Semana 4: entrega final

## 6. Call to action
Agendar kickoff em ate 7 dias uteis.

## Assinatura
consultor.teste
Assinado em [data].
"""
    p = workdir / "A-02.md"
    write(p, a02)
    add_artifact(manifest_path, "A-02", 2, "A-02.md")


def step_phase3(workdir: Path, manifest_path: Path):
    print("[4/10] Phase 3 — synthetic A-06 with 5 Whys")
    a06 = """# B-Frames Output — Empresa Sintetica Ltda

## Sintese diagnostica
[INFERÊNCIA] A queda de margem deriva de combinacao de aumento de custo
direto e perda de pricing power em 2 contratos-chave.

## 5 Porques aplicado
- Por que a margem caiu? Custos diretos subiram 12%. → [FATO]
- Por que os custos subiram? Insumos importados sofreram impacto cambial. → [FATO]
- Por que nao houve repasse? Contratos de longo prazo sem indexacao. → [FATO]
- Por que sem indexacao? Negociacao original nao previa clausula. → [INFERÊNCIA]
- Por que nao previu? Processo comercial sem padrao de risco cambial. → [INFERÊNCIA]
- Causa-raiz identificada: ausencia de politica de indexacao em contratos. → [INFERÊNCIA]

## Causas-raiz identificadas
1. [INFERÊNCIA] Ausencia de politica de indexacao contratual.
2. [HIPÓTESE] Possivel subprecificacao em servico B.

## Recomendacoes iniciais
- Implementar clausula de indexacao em renovacoes (owner: socio, prazo: 60 dias, KPI: 100% dos contratos novos com clausula).
"""
    p = workdir / "A-06.md"
    write(p, a06)
    add_artifact(manifest_path, "A-06", 3, "A-06.md")


def step_phase4(workdir: Path, manifest_path: Path):
    print("[5/10] Phase 4 — synthetic A-10 scenario table")
    a10 = """# Simulacao Phase 1 — Empresa Sintetica Ltda

## Dominio: Modelo de negocio

## Variaveis simuladas
| Variavel       | Conservador | Base   | Otimista |
|----------------|-------------|--------|----------|
| Volume mensal  | 80          | 100    | 130      |
| Margem (%)     | 6           | 9      | 13       |

## Premissas
- [FATO] Faturamento atual R$ 4,2 mi.
- [HIPÓTESE] Repasse de 50% em renovacoes 2025.

## Recomendacao derivada
Priorizar renegociacao com top-3 contratos em 90 dias.
"""
    p = workdir / "A-10.md"
    write(p, a10)
    add_artifact(manifest_path, "A-10", 4, "A-10.md")


def step_phase5(workdir: Path, manifest_path: Path):
    print("[6/10] Phase 5 — compile A-MASTER")
    cmd = [sys.executable, str(SCRIPT_DIR / "compile_master.py"),
           "--manifest", str(manifest_path),
           "--output-dir", str(workdir)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        # Print log to help diagnose.
        log = workdir / "compilation_log.md"
        if log.exists():
            print("--- compilation_log.md ---")
            print(log.read_text(encoding="utf-8"))
        raise RuntimeError(f"compile_master failed: {r.stderr}\n{r.stdout}")

    with manifest_path.open("r", encoding="utf-8") as f:
        m = yaml.safe_load(f)
    case_id = m["case_id"]
    add_artifact(manifest_path, "A-MASTER", 5, f"master_{case_id}.md")


def step_phase6(workdir: Path, manifest_path: Path):
    print("[7/10] Phase 6 — placeholder A-FINAL + A-OPS")
    final = """# Diagnostico Executivo — Empresa Sintetica Ltda

Consultor: consultor.teste
Data: 2025-04-25

## 1. Contexto
A empresa registra queda de margem nos ultimos 6 meses (verificado).

## 2. Diagnostico
Causa-raiz: ausencia de politica de indexacao em contratos (indicacao
derivada da analise).

## 3. Plano de acao
- Implementar clausula de indexacao em renovacoes.
  - Responsavel: socio fundador.
  - Prazo: 60 dias.
  - KPI: 100% dos contratos novos com clausula.

## 4. Cenarios
Conservador / Base / Otimista — ver planilha operacional anexa.

## 5. Proximos passos
Agendar kickoff em 7 dias uteis.

Assinatura
consultor.teste
Assinado em [data].
"""
    p = workdir / "A-FINAL.md"
    write(p, final)
    add_artifact(manifest_path, "A-FINAL", 6, "A-FINAL.md")

    print("[8/10] Phase 6 — generate A-OPS")
    cmd = [sys.executable, str(SCRIPT_DIR / "generate_executive_xls.py"),
           "--manifest", str(manifest_path),
           "--output", str(workdir / "A-OPS.xlsx")]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"generate_executive_xls failed: {r.stderr}")
    add_artifact(manifest_path, "A-OPS", 6, "A-OPS.xlsx")


def step_record_gates(manifest_path: Path):
    """Record G0..G3 as auto-passed for QA F18 to succeed."""
    with manifest_path.open("r", encoding="utf-8") as f:
        m = yaml.safe_load(f)
    for gid in ["G0", "G1", "G2", "G3"]:
        m.setdefault("gates_passed", []).append({
            "gate_id": gid,
            "approved_by": "consultor.teste",
            "approved_at": now_iso(),
            "hardcoded_human": gid in {"G2", "G5", "G6"},
            "reason": "dry_run synthetic auto-record",
        })
    m["gates_pending"] = ["G4", "G5", "G6"]
    m["updated_at"] = now_iso()
    with manifest_path.open("w", encoding="utf-8") as f:
        yaml.safe_dump(m, f, sort_keys=False, allow_unicode=True)


def step_validate(manifest_path: Path) -> int:
    print("[9/10] Validate QA")
    cmd = [sys.executable, str(SCRIPT_DIR / "validate_qa.py"),
           "--manifest", str(manifest_path)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(r.stdout)
    if r.stderr:
        print("STDERR:", r.stderr, file=sys.stderr)
    return r.returncode


def main() -> int:
    print("=" * 60)
    print("PRAXIS dry_run — synthetic end-to-end test")
    print("=" * 60)

    workdir = Path(tempfile.mkdtemp(prefix="praxis_dryrun_"))
    print(f"workdir: {workdir}")

    try:
        manifest_path = step_init(workdir)
        step_phase1(workdir, manifest_path)
        step_phase2(workdir, manifest_path)
        step_phase3(workdir, manifest_path)
        step_phase4(workdir, manifest_path)
        step_record_gates(manifest_path)
        step_phase5(workdir, manifest_path)
        step_phase6(workdir, manifest_path)
        qa_code = step_validate(manifest_path)

        print("[10/10] Cleanup")
        if qa_code == 0:
            print("=" * 60)
            print("RESULT: PASS")
            print("All 6 phases executed; QA returned exit 0.")
            print("=" * 60)
            shutil.rmtree(workdir, ignore_errors=True)
            return 0
        else:
            print("=" * 60)
            print(f"RESULT: PARTIAL — phases executed but QA returned exit {qa_code}.")
            print(f"Workdir kept for inspection: {workdir}")
            print("=" * 60)
            return 1
    except Exception as exc:
        print("=" * 60)
        print(f"RESULT: FAIL — {exc}")
        print(f"Workdir kept for inspection: {workdir}")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())
