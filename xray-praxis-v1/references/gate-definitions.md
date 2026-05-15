# PRAXIS — Definições de Gates

Sete gates governam o avanço do caso. Três são HARDCODED HUMAN:
G2, G5 e G6. Estes NUNCA podem ser auto-aprovados.

Documento técnico-operacional: schemas/phase-gates.yaml.

## Tabela mestre

| Gate | Local              | Tipo            | Função                                  |
|------|--------------------|------------------|-----------------------------------------|
| G0   | Fim Fase 1         | AUTO             | Intake mínimo presente ou anotado       |
| G1   | Início Fase 3      | AUTO             | A-01 normalizado com rótulos epistêmicos |
| G2   | Fim Fase 3         | HARDCODED HUMAN  | Revisão do diagnóstico                  |
| G3   | Fim Fase 4         | AUTO             | Score de prioridade computado           |
| G4   | Pré-release Fase 6 | AUTO             | QA programático (validate_qa.py)        |
| G5   | Fim Fase 6         | HARDCODED HUMAN  | Aprovação final do pacote               |
| G6   | Pós-entrega        | HARDCODED HUMAN  | Confirmação de handoff de execução      |

## G0 — Intake mínimo
Aprovado quando:
- `client_identity.company_name` está preenchido
- `briefing_path` ou `primary_problem` existe
- Cenário (A/B/C) está roteado
- Lacunas anotadas com [PENDENTE]

Falha → consultor preenche o que falta antes de avançar.

## G1 — Normalização epistêmica
Aprovado quando:
- A-01 existe no diretório do caso
- A-01 contém ao menos um rótulo [FATO], [INFERÊNCIA] ou [HIPÓTESE]

Falha → reprocessar Fase 1 antes de iniciar Fase 3.

## G2 — Revisão do diagnóstico (HARDCODED HUMAN)
Aprovado APENAS quando:
- Consultor digita literalmente "yes" via advance_phase.py
- O comando exige `--gate G2 --approved-by <consultant_id>`
- O script valida explicitamente: nunca avança em modo silencioso

Conduta esperada:
1. Consultor lê A-06 e o tier escolhido (A-07, A-08 ou A-09)
2. Consultor verifica plausibilidade de cada [INFERÊNCIA] e [HIPÓTESE]
3. Consultor confirma ou solicita reprocessamento
4. Apenas após confirmação verbal, executa o comando

Mensagem padrão do PRAXIS:
"Gate G2 requer revisão humana. Revise A-06 e o tier selecionado e
responda 'yes' para aprovar ou 'no' para retomar a fase."

## G3 — Score de prioridade
Aprovado quando:
- Ao menos um cenário simulado em A-10
- Top-3 ações com score (ex.: GUT) computado

## G4 — QA programático
Aprovado quando `scripts/validate_qa.py` retorna exit code 0.
Verifica:
- Marcadores epistêmicos presentes onde requerido
- Sem frases proibidas em deliverables de cliente
- Consistência de tokens de design
- Integridade do manifest

## G5 — Aprovação final do pacote (HARDCODED HUMAN)
Aprovado APENAS quando:
- Consultor revisou A-FINAL e A-OPS
- Consultor confirma "yes" via advance_phase.py
- O caso entra em modo "ready_to_deliver"

## G6 — Handoff de execução (HARDCODED HUMAN)
Aprovado APENAS quando:
- Cliente recebeu deliverables
- Plano de ação tem owners atribuídos
- Consultor confirma "yes" via advance_phase.py
- O caso pode ser fechado oficialmente

## Política de retomada

Caso o consultor responda "no" em G2, G5 ou G6:
- Estado é registrado em phase_history com motivo
- A fase atual permanece ativa
- Consultor pode editar artefatos manualmente
- Reapresentação ao gate requer novo `advance_phase.py`

## Auditabilidade

Cada gate aprovado registra:
- gate_id
- approved_by (consultant_id)
- approved_at (ISO timestamp UTC)
- hardcoded_human (boolean)

Esta trilha forma o Apêndice A do A-MASTER.
