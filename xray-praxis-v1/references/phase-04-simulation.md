# PRAXIS — Fase 4: Simulation

Objetivo: gerar cenários simulados (conservador, base, otimista) para
modelo de negócio, comportamento de consumidor, posição estratégica
e/ou ICP, derivando score de prioridade para o plano de ação.

Saídas: A-10 (Simulação Phase 1), A-11 (Simulação Phase 2 — opcional).

Duração típica: 1–3 horas conforme amplitude.

---

## Pré-requisitos

- Fase 3 concluída.
- Gate G2 aprovado por humano.
- A-06 disponível com causas-raiz e recomendações iniciais.

## Pipeline da Fase 4

### 4.1 — Configuração da Simulação (G-I5)
PRAXIS pergunta o domínio da simulação:
- a) Modelo de negócio (preço, custo, margem, volume)
- b) Comportamento do consumidor (jornada, retenção, churn, ticket)
- c) Posicionamento estratégico (entrada de novo segmento, mudança de canal)
- d) ICP (priorização de tipos de cliente)

Pode escolher múltiplas. Para cada escolha, o consultor fornece:
- Variáveis-alvo (quais métricas simular).
- Premissas iniciais (se houver).
- Restrições (ex.: limite de capacidade operacional).

### 4.2 — Modo da Simulação (Phase 1 ou Phase 2)

Phase 1 (A-10): simulação inicial, três cenários por dimensão:
- Conservador: pessimista mas plausível.
- Base: continuação da trajetória atual.
- Otimista: favorável mas alcançável.

Phase 2 (A-11): refinamento opcional, aplicado quando Phase 1
revela dimensão crítica que merece análise mais profunda.
Tipicamente, Phase 2 explora análise de sensibilidade — qual variável
move mais o resultado.

### 4.3 — Geração de cenários

Cada cenário é uma TABELA com:
- Variáveis de entrada (com valor).
- Cálculo intermediário.
- Métricas de saída.
- Rótulo epistêmico ([HIPÓTESE] por padrão para projeções).

Estrutura de A-10:
```
# Simulação Phase 1 — [client_company_name]

## Domínio: [Modelo de negócio | Consumidor | Estratégia | ICP]

## Variáveis simuladas
| Variável            | Conservador | Base    | Otimista |
|---------------------|-------------|---------|----------|
| Volume mensal       | 800         | 1000    | 1300     |
| Ticket médio (R$)   | 480         | 520     | 580      |
| Churn mensal        | 8%          | 5%      | 3%       |
| ...                 |             |         |          |

## Métricas derivadas
| Métrica             | Conservador | Base    | Otimista |
|---------------------|-------------|---------|----------|
| Receita mensal      | R$ 384k     | R$ 520k | R$ 754k  |
| Margem operacional  | 6%          | 9%      | 14%      |
| Caixa em 6 meses    | R$ ...      | R$ ...  | R$ ...   |

## Premissas
[FATO] / [INFERÊNCIA] / [HIPÓTESE] de cada premissa de entrada.

## Sensibilidade
Qual variável move mais o resultado.

## Recomendação derivada
Ação prioritária a partir do cenário base, com plano de
recuperação para o conservador.
```

### 4.4 — Score de prioridade
Para cada item do plano de ação herdado de Fase 3, PRAXIS calcula
um score combinando:
- GUT (Gravidade × Urgência × Tendência) — herdado de A-06.
- Impacto simulado em métrica-alvo (delta entre cenários).
- Custo de implementação (estimativa).
- Risco (probabilidade de execução falhar).

Score = (GUT × Impacto) / (Custo × Risco)

Top-N (N=3 em Basic, 5 em Lean, 8 em Full) é destacado como prioridade.

### 4.5 — Gate G3 (AUTO)

Pass critérios:
- Ao menos um cenário simulado em A-10.
- Top-3 ações com score computado.
- Cada projeção rotulada epistemicamente.

Falha → consultor preenche dado faltante e reapresenta.

---

## Subagentes invocáveis

`agents/simulator.md`: gera cenários a partir de premissas estruturadas.
Útil quando o consultor fornece variáveis em formato de tabela e quer
o trio conservador/base/otimista calculado mecanicamente.

## Casos especiais

### Simulação financeira simples (PME pequena)
Foco em:
- Fluxo de caixa mensal a 3, 6, 12 meses.
- Ponto de equilíbrio.
- Variação de ticket × volume.

### Simulação estratégica (mudança de posicionamento)
Foco em:
- Tempo de transição.
- Custo de saída do estado atual.
- Velocidade esperada de absorção pelo novo mercado.
- Risco de canibalização de receita atual.

### Simulação de ICP (priorização)
Foco em:
- LTV por tipo de cliente.
- CAC por canal de aquisição.
- Capacidade operacional alocada por segmento.
- Concentração de risco (% receita em top-N clientes).

---

## Cenário B — atualização

Em Cenário B, Fase 4 é OPCIONAL. Consultor decide:
- Manter projeções anteriores e apenas atualizá-las.
- Re-simular do zero com novos dados.
- Pular Fase 4 se o foco da revisão é apenas execução.

Se pular, G3 é registrado como "skipped (scenario B option)" e o
caso avança para Fase 5.

## Cenário C — não aplicável

Cenário C pula Fase 4 inteiramente.

---

## Recibo cognitivo de fim de fase

"Fase 4 de 6 concluída — Simulation.
 Domínios simulados: [N].
 Cenários produzidos: [N].
 Ações prioritárias com score: [N].
 Top ação: [descrição da ação #1].
 Tempo aproximado economizado: ~[N] min."

## Próximo passo

Fase 5 (Architect) — Agente 00 inicia compilação após G-I6.

## Pontos de falha conhecidos

- Premissas sem rótulo: simulação inteira é descartada e refeita.
- Cenário "otimista" sendo apenas "linear extrapolation": forçar
  premissa explícita de mudança que justifique o salto.
- Score de prioridade com divisão por zero (Custo ou Risco = 0):
  PRAXIS substitui zero por valor mínimo (ex.: 0.1) e marca a
  estimativa como [HIPÓTESE].
- Conflito entre cenário simulado e A-06: prevalece o A-06 como
  baseline; a simulação ajusta premissas para coerência.
