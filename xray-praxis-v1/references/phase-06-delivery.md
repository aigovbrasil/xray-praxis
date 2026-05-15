# PRAXIS — Fase 6: Delivery

Objetivo: produzir os deliverables finais para o cliente, aplicar
identidade visual, executar QA programático (G4) e obter as duas
aprovações humanas finais (G5 e G6).

Saídas: A-FINAL (deliverable principal designed), A-OPS (planilha
executiva XLSX).

Duração típica: 30–90 min.

---

## Pré-requisitos

- A-MASTER produzido na Fase 5.
- compilation_log.md disponível.
- consultant_config.yaml com identidade visual carregada.

## Pipeline da Fase 6

### 6.1 — Aplicação de Branding

PRAXIS lê:
- consultant_config.yaml (logo, nome, paleta override, assinatura).
- references/design-system.md (tokens fixos).

Aplica:
- Cabeçalho com logo (canto superior esquerdo, 40mm × 15mm).
- Tokens de cor (--color-primary e --color-accent override se houver;
  demais tokens fixos).
- Tipografia Inter ou fallback declarado.
- Margens A4 (top 25mm, bottom 20mm, left 25mm, right 20mm).
- Rodapé com nome do consultor, título do doc, paginação, data.

### 6.2 — Geração do A-FINAL

A-FINAL é o deliverable principal designed para o cliente. Pode ser:
- PDF (formato preferido).
- HTML designed (alternativa quando interatividade é desejada).
- Markdown formatado (fallback técnico).

Conteúdo:
- Extração APENAS de blocos marcados [TRILHA_CLIENTE] do A-MASTER.
- Blocos [TRILHA_INTERNA] excluídos.
- Marcadores epistêmicos traduzidos conforme cliente-voice.md:
  - [FATO] → "verificado", "constatado"
  - [INFERÊNCIA] → "indicação derivada da análise"
  - [HIPÓTESE] → "hipótese a validar"
- Tags `[TRILHA_CLIENTE]` removidas; conteúdo preservado.

Estrutura típica de A-FINAL (Cenários A e B):
```
# Diagnóstico Executivo — [client_company_name]

## 1. Contexto
[Sumário do contexto, sem rótulos crus]

## 2. Diagnóstico
[Causas-raiz com evidência aterrada]

## 3. Plano de Ação
[Itens 5W2H, frase imperativa, prazo, responsável, KPI]

## 4. Cenários
[Conservador / Base / Otimista, se Fase 4 executada]

## 5. Próximos Passos
[Handoff de execução]

[Bloco de assinatura do consultor]
```

Cenário C: A-FINAL é a Proposta Comercial (A-02 com branding aplicado).

### 6.3 — Geração do A-OPS

A-OPS é uma planilha XLSX executiva com 5 abas:

1. **Resumo Executivo**
   - case_id, consultant, client, date.
   - Sumário das fases.
   - Indicadores-chave.

2. **Diagnóstico**
   - Árvore de problemas com causas-raiz.
   - Rótulos epistêmicos traduzidos.
   - Score de prioridade.

3. **Plano de Ação**
   - Tabela 5W2H completa.
   - Owner, prazo, KPI.

4. **Simulação**
   - Matriz de cenários (conservador/base/otimista × métricas-chave).

5. **Próximos Passos**
   - Action items com owner, deadline, KPI, status inicial.

Tokens visuais aplicados:
- Header fill #1B2A4A com texto branco Inter 10pt bold.
- Linhas alternadas branco / #F5F7FA.
- Borda thin #D0D7E0.
- Largura mínima de coluna: 15 caracteres.
- Altura de linha: 18pt.

Geração programática via `scripts/generate_executive_xls.py` (openpyxl).

Cenário C: A-OPS NÃO é produzido.

### 6.4 — Gate G4 (AUTO — QA programático)

Executa `scripts/validate_qa.py` que verifica os 18 itens da
qa-checklist.md:

Bloco A: integridade do caso (4 checks).
Bloco B: epistemic compliance (4 checks).
Bloco C: voice compliance (4 checks).
Bloco D: design system compliance (3 checks).
Bloco E: completude do plano (2 checks).
Bloco F: governança (1 check).

Saída padrão:
```
QA Report — case_id=praxis-YYYYMMDD-XXXXXXXX
Total checks: 18
Passed: N
Failed: N
Issues:
  - [check_id] description of failure
```

- Exit code 0: G4 aprovado, avança para G5.
- Exit code 1: G4 falha, lista issues, bloqueia avanço.

Exceções:
- Consultor pode marcar checks específicos como `WAIVED` em
  manifest.qa_waivers (registrado em A-MASTER Apêndice A).
- Checks B6, B7, B8, C9, C10 não admitem waiver.

### 6.5 — Gate G5 (HARDCODED HUMAN)

PRAXIS apresenta ao consultor:
"Gate G5 requer revisão humana. Revise A-FINAL e A-OPS e responda
'yes' para aprovar a entrega ao cliente ou 'no' para retomar a fase."

Conduta esperada:
1. Consultor abre A-FINAL e revisa visualmente.
2. Consultor abre A-OPS e revisa visualmente.
3. Consultor verifica que cabeçalho, assinatura e paleta estão corretos.
4. Consultor confirma traduções epistêmicas (sem rótulos crus visíveis).
5. Executa `python scripts/advance_phase.py --gate G5 --approved-by <id>`.
6. Script exige confirmação literal "yes" em stdin.

Após G5 aprovado: caso entra em modo `ready_to_deliver`. Consultor
envia A-FINAL e A-OPS ao cliente.

### 6.6 — Gate G6 (HARDCODED HUMAN — pós-entrega)

Após o consultor confirmar que o cliente recebeu os deliverables e
que o handoff de execução foi alinhado:

PRAXIS apresenta:
"Gate G6 requer revisão humana. Confirme que o cliente recebeu os
deliverables e que o plano de ação tem owners atribuídos. Responda
'yes' para fechar o caso ou 'no' para manter aberto."

Após G6: caso é fechado oficialmente. manifest.current_phase é
mantido em 6 mas adiciona-se `closed_at: <timestamp>` no manifest.

---

## Recibo cognitivo de fim de fase

"Fase 6 de 6 concluída — Delivery.
 Artefatos finais produzidos: A-FINAL, A-OPS.
 QA G4: PASSED ([N] de 18 checks).
 Gates G5 e G6 pendentes (revisão humana obrigatória).
 Tempo aproximado economizado: ~[N] min.
 Tempo total do caso: ~[N] horas."

## Subagentes invocáveis

`agents/qa-reviewer.md`: executa QA reviewer subagent quando o
volume justifica execução isolada (Cenário A com Full tier
tipicamente).

## Pontos de falha conhecidos

- A-FINAL com rótulo cru visível: G4 bloqueia. Voltar à Fase 5 e
  re-aplicar tradução epistêmica.
- A-OPS com header em cor errada: G4 bloqueia. Re-executar
  generate_executive_xls.py com tokens corrigidos.
- consultor responde "no" em G5: PRAXIS retoma a Fase 6 e permite
  edições no A-FINAL/A-OPS antes de re-apresentar a G5.
- Logo do consultor ausente: aplicar fallback (display name em H3,
  --color-primary, alinhado à esquerda) e registrar em compilation_log.
- Cenário C em Fase 6: pular geração de A-OPS, gerar apenas A-FINAL
  como proposta com branding.
