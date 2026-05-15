# PRAXIS — Fase 3: Analytical

Objetivo: aplicar análise diagnóstica estruturada usando frameworks
selecionados, normalizar dados em formato analisável, e produzir
diagnóstico revisável até Gate G2 (HARDCODED HUMAN).

Saídas: A-05 (Normalized Data + SVG), A-06 (B-Frames Output),
e UM dos três tiers: A-07 (Basic), A-08 (Lean) ou A-09 (Full).

Duração típica: 2–6 horas conforme tier. Pode ser distribuída em
múltiplas sessões.

---

## Pré-requisitos

- A-01 aprovado e G0 passado.
- A-02/A-03/A-04 conforme cenário.
- Gate G1 (auto): A-01 contém ao menos um rótulo epistêmico.

## Pipeline da Fase 3

### 3.1 — Methodology Inject (G-I3)
Consultor pode injetar metodologia customizada:
- Texto livre: "Aplicar foco em análise de margem por linha de serviço".
- Parâmetros estruturados: setores prioritários, métricas-alvo,
  hipóteses pré-existentes do consultor.

PRAXIS registra a injeção em phase_history e a aplica como contexto
em todos os frameworks subsequentes.

### 3.2 — Wide Search (opcional)
Consultar `references/wide-search-catalog.md`.
- Cenários A e B: opcional.
- Cenário C: NÃO se aplica (Fase 3 pulada).

Quando ativada, produz fragmentos epistemicamente rotulados que são
inseridos em A-05.

### 3.3 — Tier Selection (G-I4)
PRAXIS sugere tier com base em sinais (ver b-frames-tiers.md):
- Volume de fatos coletados em Fase 1.
- Complexidade do problema declarado.
- Tempo disponível.

Consultor escolhe Basic / Lean / Full. Sugestão pode ser sobrescrita
sem justificativa.

### 3.4 — Normalização de Dados (A-05)
PRAXIS produz:
- Sumário em markdown com fatos consolidados.
- SVG opcional: árvore de problema, organograma, diagrama de fluxo.
- Cada bloco recebe rótulo epistêmico.

Estrutura de A-05:
```
# Normalized Data — [client_company_name]
## Fatos consolidados
[FATO] / [INFERÊNCIA] / [HIPÓTESE] etiquetando cada item.

## Diagrama estrutural
Referência a SVG inline ou path para arquivo.

## Wide Search (se aplicável)
Fragmentos de fontes externas, citados conforme W2 do
wide-search-catalog.md.
```

### 3.5 — Aplicação de Frameworks (B-Frames)
Conforme tier:

Basic (A-07):
- F03 GUT, F05 5W2H, F12 Ishikawa, F18 PDCA/OODA.

Lean (A-08):
- F01, F02, F03, F04, F05, F08, F12, F15, F17 (se gargalo evidente),
  F18.

Full (A-09):
- Todos os 19 frameworks (F01–F19), com os não-aplicáveis documentados
  com razão de exclusão.

Para cada framework aplicado:
- Inputs: extraídos de A-01 e A-05.
- Aplicação: subagent `diagnostic-analyzer` quando necessário.
- Output: bloco rotulado epistemicamente.
- Decisões de aplicação registradas em phase_history.

### 3.6 — Compilação do A-06 (B-Frames Output)
A-06 consolida resultados de TODOS os frameworks aplicados em
estrutura unificada:

```
# B-Frames Output — [client_company_name]

## Síntese diagnóstica
Parágrafo de 1–2 páginas com conclusão integrada.

## Frameworks aplicados
### F01 — 5 Porquês
[output do framework, com rótulos]

### F03 — GUT
[ranking]

### F12 — Ishikawa
[árvore de causas]

[... demais frameworks aplicados ...]

## Causas-raiz identificadas
Lista priorizada com rótulos.

## Recomendações iniciais
3–5 itens, formato 5W2H abreviado.

## Hipóteses a validar
Lista explícita de [HIPÓTESE] que precisam de confirmação.
```

### 3.7 — Compilação do A-07/08/09 (tier escolhido)
Profundidade conforme b-frames-tiers.md:
- A-07: 5–10 páginas.
- A-08: 15–25 páginas.
- A-09: 40–60 páginas.

A-09 inclui adicionalmente:
- SWOT completo, PESTEL, Porter, OKRs derivados.
- Lean Canvas validado.
- Customer Journey (se B2C ou se aplicável).
- Análise 7-S (se mudança organizacional em curso).

### 3.8 — Gate G2 (HARDCODED HUMAN)

PRAXIS apresenta:
"Gate G2 requer revisão humana. Revise A-06 e o tier selecionado e
responda 'yes' para aprovar ou 'no' para retomar a fase."

Conduta esperada do consultor:
1. Lê A-06 integralmente.
2. Lê o tier produzido (A-07, A-08 ou A-09).
3. Verifica plausibilidade de cada [INFERÊNCIA] e [HIPÓTESE].
4. Confirma os rótulos ou solicita reclassificação.
5. Executa `python scripts/advance_phase.py --gate G2 --approved-by <id>`.

O script valida:
- Se gate é HARDCODED_HUMAN, exige confirmação literal "yes" em stdin.
- Se consultor responde "no", gate NÃO é registrado como passado.
- Caso "no": consultor edita artefatos manualmente, então re-apresenta.

NUNCA:
- Auto-aprovar G2.
- Aceitar argumento `--auto-approve` para G2.
- Saltar G2 mesmo em modo "rapid".

---

## Subagentes invocáveis

`agents/diagnostic-analyzer.md`: aplica 5 Porquês + Pareto + GUT em
batch quando o consultor solicita análise rápida sobre conjunto
grande de problemas.

## Recibo cognitivo de fim de fase

"Fase 3 de 6 concluída — Analytical.
 Tier aplicado: [Basic|Lean|Full].
 Frameworks aplicados: [N].
 Causas-raiz identificadas: [N].
 [HIPÓTESE]s a validar: [N].
 Gate G2 pendente — revisão humana obrigatória.
 Tempo aproximado economizado: ~[N] horas."

## Próximo passo (após G2 aprovado)

Cenário A → Fase 4 (Simulation).
Cenário B → Fase 5 (Architect — pular Fase 4 se simulação não
necessária; consultor confirma).

## Pontos de falha conhecidos

- Tier Full sem dados suficientes: PRAXIS deve recusar produzir A-09
  e sugerir downgrade para Lean ou Basic, em vez de inventar
  [HIPÓTESE]s para preencher.
- Frameworks aplicados a contexto não-aplicável (ex.: 7-S em micro-PME
  de 3 pessoas): PRAXIS marca o framework como "não aplicável" e
  documenta razão.
- Wide Search retornando dado conflitante com A-01: PRAXIS prioriza
  o dado oficial (rótulo mais conservador) e registra o conflito.
