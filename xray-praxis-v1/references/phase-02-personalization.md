# PRAXIS — Fase 2: Personalization

Objetivo: produzir os artefatos comerciais e de personalização que o
consultor entregará ao cliente como parte do processo de fechamento e
onboarding.

Saídas: A-02 (Proposta Comercial), A-03 (Contrato + Showroom),
A-04 (Pacote de Personalização do Cliente).

Duração típica: 30–60 min (Cenário A); 15–30 min (Cenário B); 20–30 min (Cenário C).

---

## Pré-requisitos

- A-01 disponível e aprovado por G0.
- consultant_config.yaml com identidade do consultor (nome, logo, cores,
  contato, modelo de assinatura).

## Pipeline da Fase 2

### 2.1 — Inicialização de identidade
PRAXIS carrega:
- `consultant_display_name`
- Logo (path no consultant_config) ou fallback texto
- Tokens de cor (--color-primary, --color-accent override se houver)
- Bloco de assinatura

### 2.2 — Seleção de entregáveis (G-I2)
PRAXIS pergunta ao consultor:
"Quais entregáveis serão produzidos nesta fase?
 a) Apenas Proposta Comercial (A-02)
 b) Contrato de Fechamento + Showroom (A-03)
 c) Pacote de Personalização do Cliente (A-04)
 d) Todos os três"

A resposta determina quais sub-pipelines executar.

### 2.3 — Geração da Proposta Comercial (A-02)

Estrutura fixa de 8 seções (estrutura idêntica em Cenário A, B, C):

1. Header
   - Logo do consultor (canto superior esquerdo).
   - Cliente: nome.
   - Data de emissão.
   - Validade da proposta (30 dias por padrão).

2. Contextualização do problema
   - Parágrafo curto, resgata `primary_problem` de A-01.
   - Sem inventar dados não verificados.
   - Sem sensacionalismo.

3. Metodologia
   - 3–5 etapas previstas.
   - Tradução das fases internas do PRAXIS para linguagem consultiva
     externa (sem mencionar PRAXIS, fases internas, frameworks por nome).

4. Entregáveis
   - Lista do que o cliente recebe.
   - Quando cada item é entregue.

5. Investimento
   - Valor monetário ou [PLACEHOLDER] se ainda não definido.
   - Forma de pagamento.
   - Validade do orçamento.

6. Cronograma
   - Prazo total.
   - Marcos visíveis.

7. Call-to-Action
   - Próximo passo concreto: assinar, agendar, validar escopo.

8. Assinatura
   - Bloco do consultor.
   - Espaço para aceite do cliente.

### 2.4 — Geração do Contrato + Showroom (A-03)

Componentes:
- Contrato de prestação de serviços (template adaptável em
  assets/contrato-fechamento-template.md).
- Showroom: 1–2 páginas com casos anteriores ou prova de competência
  (sem dados confidenciais de outros clientes).

Showroom NUNCA inclui:
- Logos de outros clientes sem autorização.
- Métricas atribuídas a clientes nominais sem permissão.

Showroom PODE incluir:
- Setores atendidos (de forma anonimizada).
- Tipos de problema resolvidos.
- Resultados típicos em faixas (sem nomes).

### 2.5 — Geração do Pacote de Personalização (A-04)

A-04 é INTERNO inicialmente; pode ser entregue em parte ao cliente
após edição do consultor.

Componentes:
- Identidade visual aplicada ao cliente: paleta, tipografia, padrão
  de cabeçalho.
- Modelos de comunicação (e-mail de abertura, agenda de kickoff).
- Lista de stakeholders extraída de A-01.
- Cronograma operacional preliminar.

### 2.6 — Voz e tom
Todos os deliverables passam pelo filtro `references/cliente-voice.md`.
Verificações automáticas:
- Zero menção a IA, Claude, ChatGPT, GPT, modelo de linguagem.
- Zero emojis.
- Cabeçalho do consultor presente.
- Bloco de assinatura presente.
- Marcadores epistêmicos traduzidos para linguagem natural.

---

## Cenário C — modo proposta apenas

Quando `manifest.scenario == "C"`:
- Apenas A-02 é produzido (A-03 opcional, A-04 não produzido).
- Após Fase 2, PULAR Fase 3, 4 e 5 — ir direto para Fase 6.
- Investment frequentemente fica como [PLACEHOLDER] (consultor
  preenche manualmente antes de enviar).

## Cenário B — atualização

Quando `manifest.scenario == "B"`:
- A-02 e A-03 são OPCIONAIS (frequentemente já existem do caso anterior).
- Foco em A-04 atualizado.
- Caso o consultor já tenha contrato vigente, pular A-03.

---

## Estrutura de A-04 (Pacote de Personalização)

```
# Pacote de Personalização — [client_company_name]

## 1. Identidade visual aplicada
- Paleta primária + accent
- Tipografia (Inter por padrão, override se houver)
- Padrão de cabeçalho

## 2. Modelos de comunicação
### 2.1 E-mail de abertura
### 2.2 Agenda de kickoff
### 2.3 Padrão de relatório semanal

## 3. Stakeholders mapeados
Tabela: nome | papel | influência | atitude inicial estimada

## 4. Cronograma operacional preliminar
Marcos por fase do engajamento.

## 5. Decisões de Fase 2
Log de qualquer escolha não-trivial.
```

---

## Recibo cognitivo de fim de fase

"Fase 2 de 6 concluída — Personalization.
 Artefatos produzidos: [lista de A-02/A-03/A-04].
 Identidade visual aplicada: [paleta utilizada].
 Tempo aproximado economizado: ~40 min."

## Próximo passo

Cenário A → Fase 3 (Analytical).
Cenário B → Fase 3 (modo atualização).
Cenário C → Fase 6 (release rápido).

## Subagentes invocáveis

Nenhum em Fase 2 — fluxo principal opera direto.

## Pontos de falha conhecidos

- consultant_config.yaml ausente: PRAXIS deve solicitar configuração
  mínima (nome + cor primária + bloco de assinatura) antes de produzir.
- Logo em formato não suportado (>2MB, formato exótico): PRAXIS aceita
  PNG, JPG e SVG. Outros formatos devem ser convertidos antes.
- Investimento exigido em A-02 sem definição: usar [PLACEHOLDER] e
  registrar pendência em phase_history.
