# Executive XLSX Template — A-OPS

Este documento descreve a estrutura da planilha operacional A-OPS
gerada por `scripts/generate_executive_xls.py`. Aplica os tokens de
design definidos em `references/design-system.md`.

## Tokens visuais aplicados (programaticamente)

- Header fill: #1B2A4A (color-primary)
- Header text: branco, Inter 10pt bold
- Linhas alternadas: branco / #F5F7FA (color-surface)
- Borda: thin, #D0D7E0 (color-divider)
- Fonte do corpo: Inter 10pt
- Largura mínima de coluna: 15 caracteres
- Altura de linha: 18pt

---

## Aba 1 — Resumo Executivo

Estrutura:
- Linha 1: título mesclado (A1:E1) — "Resumo Executivo", 14pt bold,
  cor --color-primary.
- Linha 3: header da tabela (Campo | Valor).
- Linhas 4–N: pares chave/valor:
  - case_id
  - consultant_id
  - client (company_name)
  - scenario
  - current_phase
  - created_at
  - updated_at
  - artifacts_count
  - gates_passed_count

Largura sugerida: A=25, B=50.

---

## Aba 2 — Diagnóstico

Header: Problema | Causa-raiz | Rótulo | Score prioridade

Linhas: uma por causa-raiz identificada no diagnóstico (Fase 3).
Score prioridade integra GUT × Impacto / (Custo × Risco) calculado em
Fase 4.

Rótulo: traduzido para linguagem do cliente:
- [FATO] → "verificado"
- [INFERÊNCIA] → "indicação derivada"
- [HIPÓTESE] → "hipótese a validar"

Largura sugerida: A=40, B=40, C=18, D=18.

---

## Aba 3 — Plano de Ação

Header 5W2H: What | Why | Where | When | Who | How | How much

Linhas: uma por ação priorizada do plano.

Quando "Who" não está definido, valor = "[A DEFINIR]".
Quando "How much" não está estimado, valor = "[A DEFINIR]".

Largura sugerida: A=25, B=25, C=18, D=18, E=20, F=25, G=18.

---

## Aba 4 — Simulação

Header: Métrica | Conservador | Base | Otimista | Rótulo

Linhas: uma por métrica derivada de A-10 / A-11.

Métricas tipicamente incluídas:
- Receita mensal
- Margem operacional
- Caixa em 6 meses
- Volume mensal
- Ticket médio
- Churn mensal
- LTV / CAC ratio

Largura sugerida: A=30, B=18, C=18, D=18, E=18.

---

## Aba 5 — Próximos Passos

Header: Ação | Owner | Prazo | KPI | Status

Linhas: uma por item de próximos passos do A-MASTER (seção 6).

Status inicial: "pendente". Cliente atualiza durante execução.

Largura sugerida: A=40, B=25, C=18, D=25, E=15.

---

## Validação programática

Gate G4 verifica:
- D13: header da A-OPS usa #1B2A4A com texto branco — `validate_qa.py`
  confirma a presença do arquivo gerado pelo script (que aplica os
  tokens corretos por construção).

## Customização por consultor

`consultant_config.yaml` pode sobrescrever:
- `primary_color_override`: substitui --color-primary (deve ser hex
  no formato #RRGGBB).
- `accent_color_override`: substitui --color-accent.

Outros tokens (surface, divider, branco) NÃO admitem override.

## Cenários sem A-OPS

Cenário C (Proposta Comercial Rápida) NÃO produz A-OPS. O script
`generate_executive_xls.py` é chamado apenas em Cenários A e B.
