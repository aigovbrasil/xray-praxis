# PRAXIS — Modos de Decisão

Cinco modos cognitivos guiam a postura analítica do consultor em
diferentes momentos do caso. O PRAXIS roteia automaticamente sugestões
para o modo apropriado quando detecta o tipo de tarefa.

---

## EXPLORE
Postura: divergente. Gera opções sem comprometer-se.

Quando usar:
- Início de Fase 3 antes de tier selection.
- Cliente trouxe problema vago; ainda há ambiguidade sobre direção.
- Revisão estratégica em Cenário B sem hipótese forte.

Tarefas típicas:
- Brainstorm de hipóteses possíveis ([HIPÓTESE]).
- Listar segmentos/canais/ICPs candidatos.
- Mapear riscos e oportunidades.

Saída esperada:
Lista ampla, sem ranking, sem corte. Volume importa mais que precisão.

---

## EVALUATE
Postura: comparativa. Pondera opções já geradas.

Quando usar:
- Após EXPLORE, quando há lista de opções.
- Tier selection (Basic vs Lean vs Full).
- Avaliação de cenários simulados em Fase 4.

Tarefas típicas:
- Aplicar critérios (custo, prazo, risco, fit).
- Score multi-critério.
- Comparar trade-offs explícitos.

Saída esperada:
Tabela ou matriz com critérios em colunas e opções em linhas. Ranking
final justificado.

---

## DECIDE
Postura: convergente. Compromete-se com uma direção.

Quando usar:
- Final de Fase 3 antes de Gate G2.
- Definição do plano de ação prioritário.
- Aprovação ou rejeição de hipóteses.

Tarefas típicas:
- Selecionar 1 (ou poucos) caminhos a seguir.
- Registrar decisão em phase_history.
- Comunicar decisão ao cliente em linguagem direta.

Saída esperada:
Decisão única e justificada. Lista do que foi descartado e por quê
(registro de descarte é tão importante quanto a escolha).

Armadilha: pseudo-decidir mantendo várias opções "em paralelo". Decisão
real exige corte.

---

## EXECUTE
Postura: operacional. Traduz decisão em ação concreta.

Quando usar:
- Plano de ação 5W2H (Fase 3+4).
- Geração de A-OPS (Fase 6).
- Handoff para Linear/sistema de execução.

Tarefas típicas:
- Detalhar Who/When/HowMuch.
- Definir KPIs e milestones.
- Estabelecer cadência de revisão.

Saída esperada:
Item executável: um humano nomeado pode iniciar a tarefa hoje sem
perguntas adicionais.

Armadilha: ação genérica ("melhorar processo X"). Deve responder:
quem faz primeiro passo, em quanto tempo, como sabemos que terminou.

---

## REVIEW
Postura: retrospectiva. Avalia execução passada.

Quando usar:
- Cenário B (cliente retornando).
- Fase 5 quando A-MASTER prévio existe.
- Gate G6 (handoff de execução).

Tarefas típicas:
- Comparar previsto vs realizado.
- Identificar desvios.
- Atualizar hipóteses e rótulos epistêmicos.
- Promoções/rebaixamentos de [HIPÓTESE]→[INFERÊNCIA]→[FATO].

Saída esperada:
Delta documentado: o que mudou, o que foi confirmado, o que precisa
re-priorização.

---

## Roteamento automático

PRAXIS sugere modo com base em sinais textuais:

| Sinal do consultor                           | Modo sugerido |
|----------------------------------------------|----------------|
| "ainda não sei", "lista possíveis"           | EXPLORE        |
| "qual é melhor", "compara", "trade-off"      | EVALUATE       |
| "preciso decidir", "qual escolho"            | DECIDE         |
| "como faço", "monta plano", "cronograma"     | EXECUTE        |
| "o que aconteceu", "está funcionando"        | REVIEW         |

Em conflito, o consultor explicita o modo via G-I3 (methodology inject).

## Encadeamento típico em Cenário A

EXPLORE → EVALUATE → DECIDE → EXECUTE → (após dias/semanas) REVIEW

Cada modo é uma postura, não uma fase. Múltiplos modos podem ocorrer
dentro de uma única fase do caso.
