# PRAXIS — Voz do Cliente (client-facing deliverables)

Define o registro linguístico de todo artefato entregue ao cliente
final (PME). Aplica-se a A-02, A-03, A-04, A-FINAL e A-OPS.

## Princípios

- Português profissional, registro de consultor sênior brasileiro.
- Tom respeitoso, direto, sem condescendência.
- O cliente deve perceber rigor metodológico, não tecnicismo gratuito.
- Personificação apenas pelo consultor — nunca pelo PRAXIS ou Claude.

## Proibições absolutas

Nunca em deliverable de cliente:

- Qualquer menção a IA, Claude, Anthropic, modelo de linguagem, GPT,
  LLM, "gerado automaticamente", ou similares.
- Emojis.
- Linguagem corporativa vazia: "soluções inovadoras de ponta", "rumo
  ao próximo nível", "transformação 360 graus".
- Anglicismos desnecessários quando há equivalente direto em português.
- Jargão acadêmico sem aterramento em problema concreto.
- Marcadores epistêmicos internos ([FATO], [INFERÊNCIA], [HIPÓTESE])
  no formato cru. Em deliverable de cliente, traduzir para linguagem
  natural: "verificado em campo", "interpretação a partir dos dados",
  "hipótese a confirmar".

## Padrões obrigatórios

Cabeçalho:
  Identidade visual do consultor (logo + nome) no canto superior esquerdo.
  Título do documento centralizado abaixo do cabeçalho.
  Data e nome do cliente abaixo do título.

Tom de abertura:
  Frase direta sobre o objetivo do documento. Nunca "É com grande
  satisfação que..." ou similares.

Estrutura de seções:
  Numeração clara (1, 1.1, 1.2, 2, 2.1...).
  Sub-seções não excedem profundidade 3.

Citações de fontes:
  Quando referência externa (Sebrae, IBGE etc.), citar no rodapé do
  parágrafo: "Fonte: [nome], [ano]."

Recomendações:
  Sempre acompanhadas de:
  - Razão (por quê fazer)
  - Prazo sugerido
  - Responsável sugerido
  - Indicador de sucesso (KPI)

## Tradução de marcadores epistêmicos

| Interno         | Externo (cliente)                          |
|-----------------|--------------------------------------------|
| [FATO]          | "verificado", "constatado em campo"       |
| [INFERÊNCIA]    | "indicação derivada da análise"           |
| [HIPÓTESE]      | "hipótese a validar nos próximos passos"  |

Marcadores [TRILHA_INTERNA] são REMOVIDOS na geração de A-FINAL.
Marcadores [TRILHA_CLIENTE] têm o tag removido — somente o conteúdo permanece.

## Encerramento de documento

Toda entrega ao cliente termina com:

  Bloco de assinatura do consultor (nome, cargo, contato).
  Data.
  Observação sobre próximos passos ou validade da análise.

## Linguagem de proposta comercial (A-02)

Específico para Cenário C ou Fase 2:

- Problema do cliente nomeado de forma reconhecível, sem dramatizar.
- Metodologia descrita em 3–5 etapas, prazo total visível.
- Investimento como `[PLACEHOLDER]` quando ainda não definido —
  consultor preenche manualmente antes de enviar.
- CTA específico: ação clara para o cliente (assinar, agendar, validar).

## Linguagem de plano de ação (A-FINAL)

- Cada item de ação é uma frase imperativa direta.
  "Implementar controle de fluxo de caixa semanal" — sim.
  "Considerar talvez alguma forma de" — não.

- Prazos concretos: "em 30 dias", "até [data]", não "no curto prazo".

- Responsáveis nomeados quando conhecidos. Quando não conhecidos,
  usar marcador `[A DEFINIR]` que o consultor preenche.
