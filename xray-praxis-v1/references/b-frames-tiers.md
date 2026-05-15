# PRAXIS — Tiers de B-Frames (Basic / Lean / Full)

A Fase 3 produz um diagnóstico estruturado em três profundidades.
O consultor seleciona o tier via G-I4. O tier escolhido determina
qual artefato é produzido: A-07 (Basic), A-08 (Lean) ou A-09 (Full).

---

## Tier Basic (A-07)

Quando usar:
- Cliente PME pequeno (<10 funcionários, faturamento <R$ 1mi/ano).
- Briefing inicial pobre em dados.
- Cenário B (revisão) com escopo restrito.
- Restrição de tempo: análise em 1–2 horas.

Frameworks aplicados (4):
- F03 GUT (priorização)
- F05 5W2H (plano)
- F12 Ishikawa (causas-raiz)
- F18 PDCA/OODA (ciclo)

Profundidade:
- Top-3 problemas priorizados.
- 1 plano de ação com 3–5 itens.
- 1 árvore de causas-raiz.

Saída esperada (A-07):
- 5–10 páginas equivalentes em markdown.
- Mínimo 1 [FATO], 1 [INFERÊNCIA].
- [HIPÓTESE] aceitas como placeholder de validação.

---

## Tier Lean (A-08)

Quando usar:
- PME média (10–50 funcionários, faturamento R$ 1–10mi/ano).
- Cenário A com escopo focado em 1–2 vetores de problema.
- Cenário B padrão.
- Tempo disponível: 3–4 horas.

Frameworks aplicados (10):
- F01 5 Porquês
- F02 Pareto
- F03 GUT
- F04 SWOT (versão enxuta — 3 itens por quadrante)
- F05 5W2H
- F08 SCQA (estrutura narrativa do diagnóstico)
- F12 Ishikawa
- F15 RACI
- F17 TOC (apenas se gargalo evidente)
- F18 PDCA/OODA

Profundidade:
- Top-5 problemas priorizados.
- 1 plano de ação com 5–8 itens.
- 1 SWOT enxuto.
- 1–2 árvores de causas-raiz.
- Identificação de gargalo (se aplicável).

Saída esperada (A-08):
- 15–25 páginas equivalentes.
- Mínimo 3 [FATO], 3 [INFERÊNCIA].
- Cada [HIPÓTESE] acompanhada de plano de validação.

---

## Tier Full (A-09)

Quando usar:
- PME maior (50+ funcionários, faturamento >R$ 10mi/ano).
- Cenário A com problema sistêmico ou estratégico.
- Reposicionamento, fusão, transição sucessória.
- Tempo disponível: 6–8 horas distribuídas.

Frameworks aplicados (todos os 19, com exceção justificada):
- F01–F19 conforme aplicável.
- Mínimo 12 frameworks; aplicação dos demais documentada como "não
  aplicável" com razão.

Profundidade:
- Top-10 problemas priorizados.
- Plano de ação 5W2H + RACI completo.
- SWOT, PESTEL, Porter aplicados.
- OKR derivado.
- Lean Canvas validado.
- Customer Journey mapeado se aplicável.
- 7-S analisado se há mudança organizacional em curso.

Saída esperada (A-09):
- 40–60 páginas equivalentes.
- Mínimo 8 [FATO], 8 [INFERÊNCIA], 5 [HIPÓTESE] com plano de validação.
- Mínimo 3 cenários simulados em A-10.

---

## Critério de seleção (G-I4)

PRAXIS apresenta as 3 opções com tempo estimado e profundidade.
Consultor decide manualmente.

Sugestão automática do PRAXIS baseada em sinais:

| Sinal do briefing                             | Tier sugerido |
|-----------------------------------------------|----------------|
| <5 fatos coletados, problema único            | Basic          |
| 5–15 fatos, problema com 1–2 vetores          | Lean           |
| 15+ fatos, problema sistêmico/estratégico     | Full           |
| Cliente retornando (Cenário B)                | Lean (default) |
| Proposta rápida (Cenário C)                   | (não aplica)   |

A sugestão é apenas sugestão. Consultor pode override sem justificativa.

## Promoção de tier

Tier pode ser promovido durante Fase 3 (Basic → Lean → Full) se novo
material aparecer. Promoção exige:
- Registro em phase_history
- Reaplicação dos frameworks adicionais
- Reapresentação a Gate G2

Demoção é permitida mas rara — geralmente sinal de escopo mal definido.
