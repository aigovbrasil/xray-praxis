# PRAXIS

> Co-piloto de consultoria estruturada para PMEs brasileiras.
> Entregue como Claude Skill, executável em Claude.ai, Claude Code e via API.

---

## Sobre

PRAXIS é uma skill que orquestra um caso consultivo do briefing à
entrega final em 6 fases. Reduz a carga cognitiva do consultor ao
estruturar a parte repetível do trabalho — coleta, normalização,
aplicação de frameworks, simulação, compilação, QA — preservando o
julgamento humano nos pontos críticos via gates obrigatórios.

Saídas típicas de um caso completo:
- Proposta comercial assinada com identidade visual do consultor.
- Diagnóstico executivo com causas-raiz rotuladas epistemicamente.
- Plano de ação 5W2H com responsáveis, prazos e KPIs.
- Planilha operacional XLSX com cenários e próximos passos.

## Princípios operacionais

1. **Trilha epistêmica**: toda afirmação tem rótulo
   ([FATO] / [INFERÊNCIA] / [HIPÓTESE]).
2. **Hardcoded human gates**: G2, G5 e G6 nunca avançam sem
   confirmação humana.
3. **Voz dual**: consultor recebe registro técnico; cliente recebe a
   identidade do consultor, sem qualquer menção a IA.
4. **Disclosure progressiva**: PRAXIS lê apenas as referências da
   fase em curso.

## Cenários suportados

- **A — Diagnóstico Completo**: cliente novo, 6 fases, tier Full.
- **B — Revisão e Atualização**: cliente retornando, fases abreviadas.
- **C — Proposta Comercial Rápida**: 20–45 min, Fase 1 → 2 → 6.

## Instalação rápida

```bash
# 1. Descompacte praxis.zip dentro do diretório de skills do Claude
unzip praxis.zip -d ~/.claude/skills/

# 2. Instale as dependências Python
pip install pyyaml openpyxl --break-system-packages

# 3. Verifique a instalação
cd ~/.claude/skills/praxis && python scripts/dry_run.py
```

Saída esperada: `RESULT: PASS — All 6 phases executed; QA returned exit 0.`

Detalhes por plataforma em `INSTALL.md`.

## Uso básico

Em qualquer interface Claude com a skill instalada, digite:

```
novo caso PME para [nome do cliente]
```

PRAXIS abrirá o pipeline, perguntará o cenário (A / B / C) e conduzirá
fase a fase.

## Arquitetura

```
praxis/
├── SKILL.md                  Roteamento principal
├── references/  (16 .md)     Disclosure progressiva
├── agents/      (4 .md)      Subagent prompts
├── scripts/     (6 .py)      Operações deterministas
├── assets/      (5 .md)      Templates de deliverables
└── schemas/     (3 .yaml)    Manifest, registry, gates
```

Zero dependências em outras skills.

## Dependências

- Python 3.10+
- `pyyaml` 6.0+
- `openpyxl` 3.0+

## Versão

PRAXIS v1.0.0 — abril 2026.

Gaps resolvidos: GAP-01 (Agente 00), GAP-08 (Design System), GAP-09
(Cenários A/B/C).

---

# PRAXIS (English)

> Structured consulting co-pilot for Brazilian SMBs.
> Delivered as a Claude Skill — runs on Claude.ai, Claude Code, API.

## What it is

PRAXIS is a Claude Skill that orchestrates a consulting case from
intake to delivery across six phases. It reduces consultant cognitive
load by structuring the repeatable work (collection, normalization,
framework application, simulation, compilation, QA) while preserving
human judgment at critical checkpoints through mandatory gates.

Typical outputs of a full case:
- Branded commercial proposal.
- Executive diagnostic with epistemically labeled root causes.
- 5W2H action plan with owners, deadlines, KPIs.
- Operational XLSX with scenarios and next steps.

## Operating principles

1. **Epistemic trail**: every claim carries a label
   ([FATO] / [INFERÊNCIA] / [HIPÓTESE]).
2. **Hardcoded human gates**: G2, G5, G6 never auto-advance.
3. **Dual voice**: technical for consultant; client-facing carries
   the consultant's identity with no AI references.
4. **Progressive disclosure**: PRAXIS reads only the references for
   the active phase.

## Scenarios

- **A — Full Diagnostic**: new client, 6 phases, Full tier.
- **B — Review & Update**: returning client, abbreviated phases.
- **C — Fast Commercial Proposal**: 20–45 min, Phase 1 → 2 → 6.

## Quick install

```bash
unzip praxis.zip -d ~/.claude/skills/
pip install pyyaml openpyxl --break-system-packages
cd ~/.claude/skills/praxis && python scripts/dry_run.py
```

Expected output: `RESULT: PASS — All 6 phases executed; QA returned exit 0.`

See `INSTALL.md` for platform-specific details.

## Basic usage

In any Claude interface with the skill installed:

```
novo caso PME para [client name]
```

(Or English equivalent: "open new case for ..."). PRAXIS will route
to scenario selection and conduct the case.

## Architecture

```
praxis/
├── SKILL.md                  Main routing
├── references/  (16 .md)     Progressive disclosure
├── agents/      (4 .md)      Subagent prompts
├── scripts/     (6 .py)      Deterministic operations
├── assets/      (5 .md)      Deliverable templates
└── schemas/     (3 .yaml)    Manifest, registry, gates
```

Zero external skill dependencies.

## Dependencies

- Python 3.10+
- `pyyaml` 6.0+
- `openpyxl` 3.0+

## Version

PRAXIS v1.0.0 — April 2026.

Resolved gaps: GAP-01 (Agente 00), GAP-08 (Design System), GAP-09
(Scenarios A/B/C). Open gap: GAP-04 (wide-search API endpoints —
non-blocking; manual flow sufficient for v1).

## License

MIT. See LICENSE if present.
