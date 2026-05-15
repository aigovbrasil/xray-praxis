# PRAXIS — Rótulos Epistêmicos

Todo conteúdo factual no PRAXIS recebe um rótulo epistêmico explícito.
Os rótulos são preservados em todas as fases internas e traduzidos para
linguagem natural apenas em A-FINAL (deliverable de cliente).

## Os três rótulos

### [FATO]
Afirmação verificada com evidência direta.
Origem: documento, declaração explícita do cliente, dado oficial,
medição direta em campo.

Exemplos:
- [FATO] Faturamento anual de R$ 3,2 mi (declarado pelo proprietário em reunião 2025-04-12).
- [FATO] Empresa opera há 12 anos no município de Santos/SP (CNPJ 12.345.678/0001-90).
- [FATO] Equipe atual: 8 funcionários CLT.

### [INFERÊNCIA]
Conclusão derivada por raciocínio sobre dois ou mais [FATO].
Origem: aplicação de framework analítico, comparação cruzada, leitura
de padrão em dados verificados.

Exemplos:
- [INFERÊNCIA] Margem operacional provável em torno de 8% (derivada do
  faturamento declarado e da estrutura de custos relatada).
- [INFERÊNCIA] Concentração de receita em 2–3 clientes-chave indica
  exposição a risco de churn elevado.

### [HIPÓTESE]
Suposição plausível ainda não confirmada.
Origem: padrão típico do segmento, sugestão do consultor, gap detectado
no briefing que pode ser preenchido por presunção razoável.

Exemplos:
- [HIPÓTESE] Possível subprecificação do serviço B, a confirmar com
  análise de margem por linha.
- [HIPÓTESE] Rotatividade alta de equipe administrativa pode estar
  ligada à ausência de processo de onboarding estruturado.

## Regras operacionais

R1 — Toda afirmação no corpus interno (A-01, A-05, A-06, A-07/08/09)
     deve carregar exatamente UM rótulo.

R2 — Conteúdo sem fonte verificável e sem raciocínio derivativo é
     [HIPÓTESE] por padrão. Nunca presuma [FATO] sem evidência.

R3 — Promoção de rótulo (HIPÓTESE → INFERÊNCIA → FATO) só ocorre
     quando nova evidência é coletada e registrada explicitamente em
     A-01 ou em phase_history.

R4 — Rebaixamento ocorre quando evidência anterior é refutada.
     Registrar em compilation_log.md.

R5 — Em A-MASTER, Apêndice B "Trilha Epistêmica" lista TODAS as
     afirmações com seus rótulos, em ordem de produção.

R6 — Agente 00 (Phase 5, regra C5) NUNCA remove rótulos durante
     compilação. Conflitos de rótulo entre fontes são resolvidos a
     favor do rótulo MAIS CONSERVADOR (HIPÓTESE > INFERÊNCIA > FATO).

R7 — Em deliverable de cliente (A-FINAL), tradução obrigatória:
     [FATO]      → "verificado", "constatado"
     [INFERÊNCIA] → "indicação derivada da análise"
     [HIPÓTESE]  → "hipótese a validar"

## Marcadores complementares (não-epistêmicos)

[TRILHA_INTERNA] — conteúdo apenas para o consultor; removido em A-FINAL.
[TRILHA_CLIENTE] — conteúdo aprovado para o cliente; tag removido, conteúdo preservado em A-FINAL.
[PENDENTE]       — campo reconhecidamente em falta; precisa ser preenchido antes de Gate G2.
[A DEFINIR]      — placeholder ativo no plano de ação para preenchimento posterior.
[PLACEHOLDER]    — valor numérico ou textual a ser substituído pelo consultor antes do envio.

## Verificação programática

scripts/validate_qa.py verifica:
- Cada artefato com `epistemic_required: true` em artifact-registry.yaml
  contém ao menos uma ocorrência de [FATO] OU [INFERÊNCIA] OU [HIPÓTESE].
- A-MASTER contém ao menos um [FATO] (regra C7 do Agente 00).
- Em A-FINAL não há ocorrência crua de rótulos internos (todos foram
  traduzidos conforme R7).
