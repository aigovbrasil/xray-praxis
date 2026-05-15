# PRAXIS — Fase 5: Architect

Objetivo: compilar todos os artefatos produzidos até aqui em um
documento mestre (A-MASTER) com estrutura fixa, deduplicação semântica
e dual-track ([TRILHA_INTERNA] / [TRILHA_CLIENTE]).

A subroutina central da Fase 5 é o **Agente 00**, executado após
Gate G3 e diretiva G-I6.

Saídas: A-12 (Architect Pack), A-13 (Compilation Input), A-MASTER,
A-MASTER-LINEAR (opcional).

Duração típica: 30–90 min.

---

## Pré-requisitos

- Fase 3 concluída e G2 aprovado.
- Fase 4 concluída e G3 aprovado (ou pulada com registro em Cenário B).
- A-06 e tier (A-07/08/09) disponíveis.
- A-10/A-11 disponíveis (se Fase 4 executada).

## Pipeline da Fase 5

### 5.1 — G-I6: Compilation Directive
PRAXIS pergunta:
"Configure a compilação:
 - Nível de profundidade: [Resumido | Padrão | Detalhado]
 - Trilha cliente incluída? (sim/não)
 - Variáveis específicas a destacar (texto livre, opcional)
 - Gerar versão Linear? (sim/não)"

A diretiva é registrada em phase_history e usada como input pelo
Agente 00.

### 5.2 — Invocação do Agente 00 (subroutina)

Agente 00 é uma SUBROUTINA dentro da Fase 5, NÃO uma skill separada.
Implementa as 8 regras de compilação abaixo (C1–C8).

### 5.3 — Geração do A-12 (Architect Pack)
Diretório consolidando:
- A-MASTER (output principal).
- compilation_log.md (decisões do Agente 00).
- Todos os artefatos input (A-01, A-05, A-06, A-07/08/09, A-10, A-11).
- manifest.yaml snapshot.

### 5.4 — Geração opcional de A-MASTER-LINEAR
Se G-I6 marcou "Gerar versão Linear":
- Reformata A-MASTER para padrão Linear (issues + sub-issues).
- Cada item de plano de ação vira uma issue.
- Cada framework vira um doc anexado.
- Saída pronta para consumo via Linear MCP.

---

## AGENTE 00 — Regras de Compilação (GAP-01 resolvido)

Trigger: automático após Gate G3 + diretiva G-I6.

### C1 — Source resolution
Coleta artefatos em três fontes, ordem de prioridade:

1. Artefatos in-conversation (manifest.artifacts_produced[]),
   ordenados por phase ASC, depois timestamp ASC.
2. Arquivos enviados como referência pelo consultor durante o caso.
3. Documentos do Google Drive
   (manifest.client_identity.drive_references[], se MCP disponível).

Quando o mesmo conteúdo aparece em múltiplas fontes:
- Versão in-conversation vence.

### C2 — Estrutura fixa do A-MASTER

```
# [CLIENT NAME] — Dossiê Consultivo PRAXIS

## Seção 1: Contexto e Situação
(extraído de A-01)

## Seção 2: Identidade e Proposta Comercial
(extraído de A-02 / A-03 / A-04)

## Seção 3: Diagnóstico
(extraído de A-06 + tier selecionado A-07/08/09)

## Seção 4: Cenários e Simulações
(extraído de A-10 e A-11 se produzidos)

## Seção 5: Plano de Ação
(síntese de Phase 3 + Phase 4)

## Seção 6: Próximos Passos e Handoff
(itens de ação, owners, prazos)

## Apêndice A: Log de Decisões
(timestamps de gates + aprovações)

## Apêndice B: Trilha Epistêmica
(todos os rótulos FATO / INFERÊNCIA / HIPÓTESE em ordem de produção)
```

### C3 — Heading normalization
- H1 = somente título do documento.
- H2 = seções (1–6, Apêndices A e B).
- H3 = sub-tópicos dentro de seção.
- H4 = itens individuais.

Conflitos de heading no input são resolvidos antes da inserção.
Headings excedentes (H5, H6) são rebaixados para parágrafo em negrito.

### C4 — Deduplicação semântica
- Quando dois blocos têm similaridade > 80%, mantém:
  1. O mais recente (pelo timestamp).
  2. Em empate de timestamp, o de rótulo epistêmico mais específico
     ([FATO] > [INFERÊNCIA] > [HIPÓTESE]).
- Cada decisão de deduplicação é registrada em compilation_log.md
  com:
  - Bloco descartado (resumo).
  - Bloco mantido (resumo).
  - Razão.

A medição de similaridade em v1.0.0 é por sobreposição de tokens
significativos (case-folded, stop-words removidas) — heurística
simples, suficiente para v1.

### C5 — Preservação de rótulos epistêmicos
- Rótulos [FATO], [INFERÊNCIA], [HIPÓTESE] NUNCA são removidos.
- Quando uma afirmação conhecida no manifest aparece sem rótulo
  no input, o rótulo original é restaurado.
- Toda restauração é registrada em compilation_log.md.

### C6 — Dual-track inline marking
PRAXIS aplica dois marcadores ao longo do A-MASTER:

- `[TRILHA_INTERNA]` — conteúdo apenas para o consultor.
  Incluído no ZIP de auditoria. NÃO usado em A-FINAL.

- `[TRILHA_CLIENTE]` — conteúdo aprovado para o cliente.
  Usado pelo Phase 6 ao gerar A-FINAL. Tag é removida; o conteúdo
  permanece.

Conteúdo SEM marcador explícito assume regra:
- Seções 1–6 do corpo principal: default [TRILHA_CLIENTE].
- Apêndices A e B: default [TRILHA_INTERNA].

### C7 — Verificação de completude mínima

Antes de produzir A-MASTER, Agente 00 valida:
- [ ] Seção 1 contém ≥ 3 campos normalizados de A-01.
- [ ] Seção 3 contém ≥ 1 causa-raiz identificada.
- [ ] Seção 5 contém ≥ 1 item de ação com owner + prazo.
- [ ] ≥ 1 rótulo [FATO] presente em todo o documento.

Se algum check falha:
- Agente 00 NÃO produz A-MASTER.
- Retorna ao consultor com lista exata dos elementos faltantes.
- Consultor edita artefatos input ou adiciona conteúdo manualmente.
- Re-executa Agente 00.

### C8 — Output

- Arquivo: `master_<case_id>.md` (UTF-8).
- Arquivo de log: `compilation_log.md` (UTF-8).
- Ambos no diretório do caso, registrados em
  `manifest.artifacts_produced[]`.

---

## Recibo cognitivo de fim de fase

"Fase 5 de 6 concluída — Architect.
 A-MASTER gerado: master_<case_id>.md.
 Decisões registradas em compilation_log.md: [N].
 Trilha cliente identificada: [N] blocos.
 Trilha interna identificada: [N] blocos.
 Tempo aproximado economizado: ~[N] min."

## Próximo passo

Fase 6 (Delivery) — branding + A-FINAL + A-OPS + Gate G4 + G5 + G6.

## Subagentes invocáveis

`agents/document-compiler.md`: implementa Agente 00 com as regras
C1–C8. Invocado quando o volume de artefatos justifica execução
em subagent dedicado.

## Pontos de falha conhecidos

- C7 falha por falta de [FATO]: indica que a Fase 1 não capturou
  evidências verificáveis. Voltar à Fase 1 ou adicionar fato manualmente.
- Conflito de rótulo entre fontes (mesmo claim com [FATO] em A-01 e
  [HIPÓTESE] em A-06): aplicar regra de rótulo MAIS CONSERVADOR
  ([HIPÓTESE] vence) e registrar em compilation_log.md.
- Tamanho do A-MASTER excede 100 páginas: PRAXIS oferece geração de
  versão "Resumida" automaticamente (extrai apenas marcadores
  [TRILHA_CLIENTE] + sumário executivo).
