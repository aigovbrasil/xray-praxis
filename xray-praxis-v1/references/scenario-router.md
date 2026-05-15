# PRAXIS — Roteador de Cenários (A / B / C)

Resolve GAP-09. Define os três cenários operacionais e suas regras
de pipeline, gates ativos, tier default, duração estimada e A-02
(quando aplicável).

A escolha do cenário ocorre em G-I1 (início da Fase 1).

---

## Cenário A — Diagnóstico Completo

Quando usar:
- Cliente novo.
- Problema ainda não compreendido em profundidade.
- Engajamento consultivo completo planejado.

Triggers do consultor:
- "novo cliente"
- "diagnóstico completo"
- "engajamento completo"

Pipeline:
- Todas as 6 fases obrigatórias.
- Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6.
- Subroutina Agente 00 acionada na Fase 5 após G3.

Tier default: Full (A-09).
Frameworks: todos os 19 são candidatos.

Corpus produzido:
- A-01 (intake completo)
- A-02 + A-03 + A-04 (entregáveis comerciais)
- A-05 + A-06 + A-09 (diagnóstico Full)
- A-10 + A-11 (simulações)
- A-MASTER + A-FINAL + A-OPS

Gates ativos:
- G0, G1, G2, G3, G4, G5, G6 — todos.
- G2, G5, G6 hardcoded humanos.

Duração estimada: 4–8 horas distribuídas em 1–3 sessões.

---

## Cenário B — Revisão e Atualização

Quando usar:
- Cliente que já passou por Cenário A (ou diagnóstico anterior).
- Atualização de diagnóstico existente.
- Acompanhamento de progresso de plano de ação.
- Necessidade de delta entre estado anterior e atual.

Triggers do consultor:
- "retomar caso"
- "atualizar diagnóstico"
- "cliente que já atendi"

Pipeline (abreviado):
- Phase 1 (abreviada) → Phase 3 (atualização) → Phase 5 (delta merge) → Phase 6.
- Phase 2 e Phase 4 são OPCIONAIS.

Phase 1 abreviada:
- Coleta de mudanças desde último contato.
- Re-rotulação epistêmica de hipóteses anteriores (promoção/rebaixamento).
- Coleta de novos dados (resultados de ações executadas).

Phase 5 delta merge:
- Carrega A-MASTER anterior via `case_id_previous` no manifest.
- Compara estado anterior vs atual.
- Produz novo A-MASTER com seção "Delta desde [data]" no Apêndice A.

Tier default: Lean (A-08).

Corpus produzido:
- A-01 (delta)
- A-08 (atualizado)
- A-MASTER (com delta) + A-FINAL + A-OPS

Gates ativos:
- G0 (abreviado): basta confirmar mudanças relevantes.
- G1, G2, G5: OBRIGATÓRIOS.
- G3, G4, G6: OPCIONAIS.

Duração estimada: 1.5–3 horas.

---

## Cenário C — Proposta Comercial Rápida

Quando usar:
- Acabou de sair de reunião com prospect.
- Janela de oportunidade curta.
- Necessidade de proposta antes do interesse esfriar.
- Não há tempo para diagnóstico completo nesta etapa.

Triggers do consultor:
- "proposta rápida"
- "só quero gerar proposta"
- "qualificar oportunidade"

Pipeline:
- Phase 1 (5 campos obrigatórios) → Phase 2 (foco em proposta) → Phase 6.
- Phase 3, Phase 4 e Phase 5 PULADAS.

Phase 1 — campos obrigatórios (apenas estes 5):
1. company_name
2. segment
3. primary_problem
4. urgency_level
5. decision_makers

Outros campos: deixar como [PENDENTE].

Phase 2 — foco exclusivo em A-02 (Proposta Comercial).
A-03 é opcional. A-04 não é produzido.

A-02 deve conter as seguintes seções (estrutura fixa):
1. header (cabeçalho com logo do consultor + data + cliente)
2. problem contextualization (parágrafo curto, sem inventar dados)
3. methodology (3–5 etapas previstas)
4. deliverables (lista do que o cliente recebe)
5. investment [PLACEHOLDER] (consultor preenche manualmente)
6. timeline (prazos estimados por etapa)
7. CTA (call-to-action específico)
8. signature (bloco de assinatura)

Phase 6:
- Aplica branding do consultor.
- Gera A-FINAL versão da proposta.
- A-OPS NÃO é produzido neste cenário (pular geração).

Corpus produzido:
- A-01 (mínimo)
- A-02 (proposta)
- A-03 (opcional, contrato)
- A-FINAL (proposta com branding)

Gates ativos:
- G0 apenas (com critério reduzido para 5 campos).
- G1, G2, G3, G4, G5, G6: PULADOS ou auto-aprovados sem revisão substancial.

Duração estimada: 20–45 minutos.

Pós-aceite do cliente:
Se o cliente aceitar a proposta, INICIAR um novo caso em Cenário A
para diagnóstico completo. O caso de Cenário C é encerrado e
arquivado como "proposal_only".

---

## Tabela de seleção rápida

| Necessidade                                 | Cenário | Duração |
|---------------------------------------------|---------|---------|
| Cliente novo, escopo amplo                  | A       | 4–8h    |
| Cliente retornando, atualizar diagnóstico   | B       | 1.5–3h  |
| Pós-reunião, proposta urgente               | C       | 20–45m  |

## Override manual

O consultor pode escolher qualquer cenário independentemente da
sugestão automática do PRAXIS. A escolha é registrada em
`manifest.scenario` e auditável em `phase_history`.
