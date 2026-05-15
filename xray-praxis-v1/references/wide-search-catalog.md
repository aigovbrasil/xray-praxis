# PRAXIS — Catálogo de Fontes de Wide Search

A Fase 3 (analítica) pode acionar busca externa para enriquecer o
contexto do caso com dados públicos brasileiros.

Status: catálogo de fontes definido; endpoints de API e modos de
acesso programático permanecem em aberto (ver BUILD_NOTES.md, GAP-04).

## Fontes oficiais brasileiras (PME)

### Sebrae
URL base: https://sebrae.com.br
Tipo: portal de conteúdo + relatórios setoriais.
Uso típico: benchmarks por segmento, perfil de PMEs por região, estudos
de mercado nacional.
Acesso programático: limitado. Consultor coleta manualmente; PRAXIS
processa o texto colado.

### IBGE
URL base: https://www.ibge.gov.br
APIs públicas: https://servicodados.ibge.gov.br/api/docs (não
catalogadas exaustivamente neste documento — ver GAP-04).
Uso típico: PIB municipal, demografia, classificação de atividade
econômica (CNAE), pesquisa de comércio e serviços.

### MDIC (Ministério do Desenvolvimento, Indústria, Comércio e Serviços)
URL base: https://www.gov.br/mdic
Uso típico: balanço comercial, dados de exportação/importação por NCM,
políticas industriais.

### Receita Federal
URL base: https://www.gov.br/receitafederal
Uso típico: validação de CNPJ, situação cadastral, regime tributário.
Acesso programático: API pública limitada via Receitaws e
similares (verificar termos de uso).

### Junta Comercial (cada estado)
URL base: variável por UF (JUCESP, JUCERJA, JUCEMG etc.).
Uso típico: estrutura societária, alterações contratuais, estado da empresa.

### Banco Central do Brasil
URL base: https://www.bcb.gov.br
APIs públicas: SGS (Sistema Gerenciador de Séries Temporais).
Uso típico: taxa Selic, IPCA, câmbio, inadimplência setorial.

### CNI / FIESP / federações estaduais
URLs variáveis.
Uso típico: indicadores industriais setoriais, sondagens de confiança.

### Boletim Focus (BCB)
URL: https://www.bcb.gov.br/publicacoes/focus
Uso típico: expectativa de mercado para inflação e crescimento — útil
para Fase 4 (simulação macro).

## Fontes setoriais (uso conforme briefing)

### ANVISA
Para clientes em alimentos, cosméticos, medicamentos.

### ANATEL
Para clientes em telecomunicações.

### Banco Central — Open Banking / PIX stats
Para clientes em fintechs ou que dependem de meios de pagamento.

### Procon estaduais
Para clientes em B2C com sensibilidade reputacional.

### Reclame Aqui
Para clientes em B2C com presença digital.

## Tipos de busca

### Tipo 1 — Benchmark setorial
Inputs: CNAE primário, faixa de faturamento, região.
Outputs: faixa típica de margem, ciclo de caixa, ticket médio.
Marcadores: [INFERÊNCIA] (derivada de fonte) ou [HIPÓTESE] (extrapolada).

### Tipo 2 — Validação cadastral
Inputs: CNPJ.
Outputs: razão social, situação, atividade primária/secundária, abertura.
Marcador: [FATO] se fonte oficial.

### Tipo 3 — Macroindicadores
Inputs: período, indicador.
Outputs: série temporal, projeção.
Marcador: [FATO] (histórico) ou [HIPÓTESE] (projeção).

### Tipo 4 — Concorrência
Inputs: nome do mercado, região.
Outputs: lista de players visíveis, posicionamento aparente.
Marcador: [INFERÊNCIA] (compilação de fontes) ou [HIPÓTESE] (lacunas).

## Política de uso

W1. Toda informação trazida por wide search recebe rótulo epistêmico
    explícito antes de ser inserida em A-05 ou A-06.

W2. Fonte é citada no formato:
    "Fonte: [nome], [ano], URL acessada em [data]."

W3. Wide search é OPCIONAL em Cenários A e B. NUNCA usado em Cenário C
    (proposta rápida).

W4. Quando endpoints programáticos não estão disponíveis, o consultor
    cola conteúdo manualmente e o PRAXIS normaliza.

W5. PRAXIS não inventa números. Se não há fonte verificável, o campo
    permanece como [PENDENTE] até o consultor preencher.

## Gap técnico aberto (GAP-04)

A automação programática de wide search depende de:
- Catálogo de endpoints de API por fonte (em mapeamento)
- Política de rate limit
- Mecanismo de cache local
- Tradução de respostas API para formato A-05

Este gap é não-bloqueante. O fluxo manual (consultor cola, PRAXIS
normaliza) é suficiente para v1.0.0.
