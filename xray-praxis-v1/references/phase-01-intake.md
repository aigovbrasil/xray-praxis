# PRAXIS — Fase 1: Intake

Objetivo: transformar briefing bruto, notas de reunião ou texto livre
em um corpus normalizado e epistemicamente rotulado, com cenário
roteado e Gate G0 aprovado.

Saída: artefato A-01 (Normalized Follow Up).
Duração típica: 15–60 min (Cenário A); 5–15 min (Cenário B); 5–10 min (Cenário C).

---

## Entradas aceitas

- Briefing escrito pelo consultor.
- Transcrição de reunião.
- Notas livres.
- Documentos uploaded (PDF, DOCX) — extraídos antes da normalização.
- Referências de Google Drive (via MCP, se disponível).

## Pipeline da Fase 1

### 1.1 — Boot do caso
- Executar `scripts/init_case.py` para gerar manifest.yaml.
- Coletar consultor_id e client.company_name.
- Anexar `briefing_path` se houver arquivo.

### 1.2 — Roteamento de cenário (G-I1)
PRAXIS pergunta:
"Qual o tipo de atendimento?
 a) Diagnóstico Completo (cliente novo)
 b) Revisão e Atualização (cliente retornando)
 c) Proposta Comercial Rápida (pós-reunião)"

A resposta define o pipeline subsequente — ver scenario-router.md.

### 1.3 — Extração de campos
PRAXIS lê o briefing e extrai (quando presente):
- company_name (obrigatório em todos os cenários)
- segment
- cnpj
- city / state
- employees
- annual_revenue_brl
- decision_makers
- primary_problem
- urgency_level
- secondary_problems
- prior_consulting_history

Campos ausentes recebem marcador [PENDENTE].

### 1.4 — Rotulagem epistêmica
Cada afirmação extraída recebe um rótulo conforme epistemic-labels.md:
- [FATO] = declaração explícita do cliente, dado oficial
- [INFERÊNCIA] = derivação razoável de 2+ fatos
- [HIPÓTESE] = padrão típico ou suposição plausível

### 1.5 — Identificação de lacunas
PRAXIS lista campos [PENDENTE] e sugere ao consultor:
- Quais campos pode preencher manualmente agora.
- Quais devem ser confirmados com o cliente.
- Quais podem ser deixados em aberto (caso minor).

### 1.6 — Gate G0
Pass critérios:
- company_name preenchido
- briefing_path OU primary_problem existe
- scenario ∈ {A,B,C}
- lacunas anotadas com [PENDENTE]

Se passar: emite recibo de fase e avança.
Se falhar: lista exatamente o que falta e bloqueia avanço.

---

## Estrutura do A-01 (Normalized Follow Up)

```
# Normalized Follow Up — [client_company_name]
## Identidade do cliente
[FATO] / [INFERÊNCIA] / [HIPÓTESE] etiquetando cada campo.

## Problema primário
Descrição. Rótulo.

## Problemas secundários
Lista. Cada item rotulado.

## Stakeholders / decision_makers
Quem decide. Quem opera. Quem é afetado.

## Histórico consultivo
Engajamentos anteriores se houver.

## Lacunas identificadas
Lista de [PENDENTE] com sugestão de coleta.

## Cenário roteado
A / B / C. Justificativa.

## Decisões de Fase 1
Registro de qualquer escolha não-trivial feita pelo PRAXIS.
```

---

## Variantes por cenário

### Cenário A
Coleta completa. Todos os campos tentados. Lacunas aceitas com plano
de preenchimento. Tier sugerido será definido apenas em G-I4 (Fase 3).

### Cenário B
Foco em DELTAS desde o último contato:
- O que mudou desde última análise?
- Quais ações foram executadas?
- Quais resultados foram observados?
- Quais hipóteses foram confirmadas/refutadas?

PRAXIS tenta carregar `case_id_previous` automaticamente se o
consultor mencionar caso prévio.

### Cenário C
Coleta MÍNIMA — apenas 5 campos:
1. company_name
2. segment
3. primary_problem
4. urgency_level
5. decision_makers

Demais campos: [PENDENTE] aceito sem precisar plano de preenchimento.

---

## UX: condução da entrevista

PRAXIS NUNCA dispara dezenas de perguntas de uma vez. Aplica:
- Uma pergunta por turno.
- Opções clicáveis quando a resposta é finita.
- Texto livre quando o input é aberto.
- Após cada resposta, atualiza o A-01 incrementalmente.

Exemplo de turno:
"Identifiquei que o problema primário declarado é 'queda de margem
em 18% nos últimos 6 meses'. Confirma como [FATO] (cliente declarou
explicitamente) ou prefere marcar como [INFERÊNCIA] (sua leitura)?"

## Recibo cognitivo de fim de fase

Mensagem padrão ao consultor ao concluir Fase 1:

"Fase 1 de 6 concluída — Intake.
 Artefatos produzidos: A-01.
 Cenário roteado: [A|B|C].
 Lacunas registradas: [N] campos [PENDENTE].
 Tempo aproximado economizado em comparação à execução manual: ~25 min."

## Próximo passo

Se cenário A ou B → Fase 2 (Personalization).
Se cenário C → Fase 2 (modo proposta apenas) → Fase 6.

## Subagentes invocáveis

Nenhum subagente é estritamente necessário em Fase 1. PRAXIS opera o
fluxo principal direto.

## Pontos de falha conhecidos

- Briefing extremamente curto (<200 caracteres): PRAXIS deve recusar
  seguir e pedir mais contexto, em vez de inventar [HIPÓTESE]s.
- Briefing em outro idioma: traduzir antes de extrair, ou pedir
  briefing em português.
- Briefing em PDF escaneado: usar pdf-reading skill para OCR antes de
  iniciar Fase 1.
