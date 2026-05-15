# BUILD_NOTES — PRAXIS v1.0.0

Registra decisões de arquitetura, gaps endereçados e gaps em aberto.
Documento auditável; cada release atualiza esta lista.

---

## Status dos GAPS conhecidos

### GAP-01 — Agente 00 ✅ RESOLVED

**Problema original**: a Fase 5 mencionava um "Agente 00" responsável
por compilar o A-MASTER, mas as regras de compilação não estavam
formalizadas, gerando ambiguidade sobre source resolution, deduplicação,
preservação de rótulos e gates de completude.

**Resolução**: Agente 00 é formalizado como **subroutina de Fase 5**
(não skill separada) com 8 regras explícitas, C1..C8:

- C1 — source resolution com prioridade in-conversation > uploads > Drive.
- C2 — estrutura fixa do A-MASTER (Seções 1–6 + Apêndices A e B).
- C3 — heading normalization.
- C4 — deduplicação semântica (similaridade > 0.80, mais recente vence,
       desempate por rótulo mais específico).
- C5 — preservação de rótulos epistêmicos.
- C6 — dual-track inline marking ([TRILHA_INTERNA] / [TRILHA_CLIENTE]).
- C7 — minimum completeness check (4 sub-checks; falha bloqueia
       produção do A-MASTER).
- C8 — output (`master_<case_id>.md` + `compilation_log.md`).

**Implementação**:
- Especificação em `references/phase-05-architect.md`.
- Subagent prompt em `agents/document-compiler.md`.
- Implementação determinística em `scripts/compile_master.py`.

**Verificação**: `dry_run.py` exercita C1..C8 com dados sintéticos.
Após patch (split_into_blocks + demote_block_heading) o C7 retorna
PASS em todos os 4 sub-checks com input mínimo válido.

---

### GAP-08 — Design System ✅ RESOLVED

**Problema original**: deliverables careciam de identidade visual
unificada; tokens de cor e tipografia não estavam declarados, e a
parametrização por `consultant_config.yaml` era ambígua.

**Resolução**: design system fixo, com tokens declarados em
`references/design-system.md`:

- Paleta navy/sage/sand:
  - `--color-primary: #1B2A4A`
  - `--color-accent: #2E7D9B`
  - `--color-positive: #1A6B42` (mapeia [FATO])
  - `--color-neutral: #5C6B7A` (mapeia [INFERÊNCIA])
  - `--color-caution: #8B5E00` (mapeia [HIPÓTESE])
  - `--color-surface: #F5F7FA`
  - `--color-divider: #D0D7E0`
- Tipografia: Inter (heading 600, body 400, line-height 1.6).
  Fallback: stack do sistema com declaração explícita.
- Layout A4: margens 25/20/25/20 mm, conteúdo 165 mm de largura útil.
- Override: APENAS `primary_color_override` e `accent_color_override`
  via `consultant_config.yaml`.

**Implementação**:
- `references/design-system.md` (canônico).
- `scripts/generate_executive_xls.py` aplica os tokens
  programaticamente (header `#1B2A4A`, alternância
  `#FFFFFF` / `#F5F7FA`, borda `#D0D7E0`, Inter 10pt).
- `assets/executive-xls-template.md` documenta a estrutura.

**Verificação**: gate G4 (validate_qa.py) inclui checks D13–D15 que
verificam a aplicação dos tokens nos deliverables produzidos.

---

### GAP-09 — Cenários A / B / C ✅ RESOLVED

**Problema original**: o pipeline assumia caso novo, mas consultores
relatavam dois fluxos adicionais comuns: revisão de caso anterior e
proposta comercial rápida sem diagnóstico prévio. O comportamento da
skill nessas situações era indefinido.

**Resolução**: três cenários formalizados, cada um com pipeline
distinto:

- **Cenário A — Diagnóstico Completo**:
  Pipeline: 1 → 2 → 3 → 4 → 5 → 6.
  Tier default: Full (A-09).
  Gates aplicáveis: todos (G0..G6).

- **Cenário B — Revisão e Atualização**:
  Pipeline: 1 → 3 (delta) → 4 (opcional) → 5 → 6.
  Vincula `case_id_previous`. Compilação inclui seção "Delta desde
  A-MASTER anterior" no Apêndice A.
  Tier típico: Lean (A-08).

- **Cenário C — Proposta Comercial Rápida**:
  Pipeline: 1 → 2 → 6.
  Sem A-OPS. A-FINAL é a proposta com branding aplicado.
  Duração-alvo: 20–45 minutos.
  Gates: G0, G4 (modo light), G5, G6.

**Implementação**:
- `references/scenario-router.md` (canônico).
- G-I1 apresentado em Fase 1, antes da coleta substantiva.
- `init_case.py --scenario A|B|C` registra o cenário no manifest.
- Cada referência de fase contém uma seção "Variantes de cenário"
  ajustando o comportamento.

**Verificação**: `validate_qa.py` aplica check F18 com requisitos
diferenciados por cenário (gates obrigatórios variam: A exige G0..G3
em F18, B exige G0..G2, C exige apenas G0).

---

### GAP-04 — Wide Search API endpoints ⚠ OPEN (non-blocking)

**Problema original**: a Fase 3 admite consulta a fontes externas
(Sebrae, IBGE, MDIC, BCB) via subroutina "wide search", mas os
endpoints programáticos não estão catalogados.

**Status atual**: NÃO BLOQUEANTE para v1.0.0.

**Mitigação**: o fluxo manual está documentado em
`references/wide-search-catalog.md` — o consultor consulta as fontes
diretamente, traz fragmentos para a conversa, e PRAXIS os integra ao
A-05 com rótulo epistêmico. Esse fluxo é suficiente para casos A/B/C
em v1.0.0.

**Plano para v1.1**: catalogar endpoints (Sebrae Open Data, IBGE
Sidra API, BCB SGS, MDIC Comex) e adicionar `scripts/wide_search.py`
para consulta programática com cache local.

---

## Decisões de arquitetura

### D-1 — Single-skill vs multi-skill
Decisão: single-skill com disclosure progressiva. Justificativa:
mantém o caso coeso, evita acoplamento entre skills, e a tabela de
disclosure em SKILL.md é leve o bastante para roteamento sem custo
significativo.

### D-2 — Subagent format
Decisão: cada subagent é um arquivo `.md` em `agents/` com seções
`<identity><rules><input_contract><output_contract><quality_bar>`.
Justificativa: formato auto-contido, prompt-portável, e auditável
linha a linha.

### D-3 — Hardcoded human gates
Decisão: G2, G5, G6 são marcados como hardcoded em
`schemas/phase-gates.yaml`, e `advance_phase.py` rejeita
`--auto-confirm` para esses gates (exit code 3). Justificativa:
proteção contra automação inadvertida; preserva responsabilidade do
consultor sobre decisões críticas (aprovação de diagnóstico,
aprovação de entregáveis, fechamento do caso).

### D-4 — Manifest como single source of truth
Decisão: `manifest.yaml` é o único estado persistente do caso. Todo
script lê e/ou atualiza o manifest. Não há banco de dados, cache
externo ou estado em variáveis de ambiente. Justificativa:
portabilidade entre Claude.ai / Claude Code / API; auditabilidade
trivial.

### D-5 — Templates como markdown
Decisão: templates em `assets/` são markdown com placeholders
`{{var}}` em vez de Jinja ou similares. Justificativa: zero
dependências, legibilidade, suficiente para v1.0.0. Migração para
template engine só se justificará com lógica condicional não-trivial.

### D-6 — Dependência mínima de Python
Decisão: apenas `pyyaml` e `openpyxl`. Sem pandas, numpy, requests.
Justificativa: instalação trivial, sandbox-friendly, surface de
ataque mínima.

---

## Verificação contínua

`scripts/dry_run.py` é o teste end-to-end canônico. Executa:

1. init_case com cliente sintético.
2. Phase 1: A-01 com [FATO]/[INFERÊNCIA]/[HIPÓTESE].
3. Phase 2: A-02 (proposta).
4. Phase 3: A-06 com 5 Whys.
5. Phase 4: A-10 (cenários).
6. Registro de gates G0..G3 (não-humanos no contexto de teste).
7. Phase 5: compile_master.py → A-MASTER + compilation_log.md.
8. Phase 6: A-FINAL placeholder + A-OPS via XLSX generator.
9. validate_qa.py contra o caso completo.

Resultado válido: `RESULT: PASS — All 6 phases executed; QA returned exit 0.`

Para regressão, executar antes de cada commit/release.

---

## Histórico de versões

### v1.0.0 — abril 2026
Primeira release. Resolve GAP-01, GAP-08, GAP-09. Mantém GAP-04 em
aberto com mitigação manual. Skill auto-suficiente, zero
dependências em outras skills.
