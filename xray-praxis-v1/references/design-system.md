# PRAXIS — Design System

Resolve GAP-08. Especifica identidade visual aplicada a todo
deliverable de cliente (A-02, A-03, A-04, A-FINAL, A-OPS).

A consultoria pode sobrescrever cores `--color-primary` e
`--color-accent` via `consultant_config.yaml`. Os demais tokens
permanecem fixos.

---

## Paleta de cores

| Token                | Hex      | Uso                                      |
|----------------------|----------|------------------------------------------|
| --color-primary      | #1B2A4A  | Cabeçalhos, títulos                      |
| --color-accent       | #2E7D9B  | Destaques, links                         |
| --color-positive     | #1A6B42  | Rótulo [FATO], métricas positivas        |
| --color-neutral      | #5C6B7A  | Rótulo [INFERÊNCIA], texto secundário    |
| --color-caution      | #8B5E00  | Rótulo [HIPÓTESE], suposições            |
| --color-surface      | #F5F7FA  | Fundo, linhas alternadas em tabelas      |
| --color-divider      | #D0D7E0  | Bordas, réguas                           |
| --color-text         | #1C2430  | Corpo                                    |
| --color-text-muted   | #6B7685  | Notas, metadados                         |

Override do consultor:
- `consultant_config.yaml` aceita campos `primary_color_override` e
  `accent_color_override` no formato hex (#RRGGBB).
- Tokens restantes não admitem override.

---

## Tipografia

```
--font-heading: Inter, sans-serif | weight 600
--font-body:    Inter, sans-serif | weight 400 | line-height 1.6
--font-mono:    JetBrains Mono, monospace
```

Tamanhos:
- H1 = 24px
- H2 = 18px
- H3 = 14px
- Corpo = 11px
- Caption = 9px

Fallback (quando Inter não disponível):
`Inter, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif`

---

## Layout (formato A4)

Página: 210mm × 297mm (retrato).
Margens:
- Top: 25mm
- Bottom: 20mm
- Left: 25mm
- Right: 20mm

Largura de conteúdo: 165mm.
Gutter de coluna (quando 2 colunas): 6mm.

Espaçamento:
- Entre seções: 8mm
- Entre parágrafos: 4mm

---

## Logo e identidade

Posição: canto superior esquerdo.
Bounding box: 40mm × 15mm.

Fallback (quando consultoria não fornece logo):
- Texto: `consultant_display_name` do consultant_config.yaml.
- Tamanho: H3.
- Cor: --color-primary.
- Alinhamento: à esquerda.

PROIBIDO:
- Logo centralizado.
- Logo no rodapé.
- Logo inline com corpo de texto.
- Logo com proporções distorcidas.

---

## Tabelas

- Header: fundo --color-primary, texto branco, weight 600.
- Linhas: alternadas branco / --color-surface.
- Borda: 0.5px sólida --color-divider.
- Padding interno: 4px vertical, 8px horizontal.

---

## Call-out de [HIPÓTESE]

- Borda esquerda: 3px sólida --color-caution.
- Fundo: #FFF8EC.
- Padding: 8px 12px.
- Espaçamento vertical: 4mm acima e abaixo.

Quando [HIPÓTESE] aparece em deliverable de cliente, é traduzida para
"Hipótese a validar" mas mantém o mesmo estilo visual de call-out.

---

## Badges epistêmicas (uso interno; convertidas em A-FINAL)

- [FATO]: fundo --color-positive, texto branco, weight 600, 9px.
- [INFERÊNCIA]: fundo --color-neutral, texto branco, weight 600, 9px.
- [HIPÓTESE]: fundo --color-caution, texto branco, weight 600, 9px.

Border-radius: 2px. Padding: 1px 4px.

---

## Rodapé de página

Esquerda: nome do consultor.
Centro: título do documento.
Direita: "Página N de M" + data ISO.

Cor: --color-text-muted. Tamanho: caption (9px).
Régua superior: 0.5px --color-divider.

---

## XLSX (A-OPS)

Header da tabela:
- Fill: #1B2A4A
- Texto: branco, Inter 10pt, bold
- Alinhamento: centro/esquerda conforme tipo de coluna

Corpo:
- Linhas alternadas: branco e #F5F7FA
- Borda: thin, #D0D7E0
- Fonte: Inter 10pt
- Largura mínima de coluna: 15 caracteres
- Altura de linha: 18pt

Aba "Resumo Executivo":
- Mescla células do título (linha 1, colunas A–E)
- Título em --color-primary, 14pt bold

---

## Tokens em CSS (quando renderizado em HTML)

```css
:root {
  --color-primary: #1B2A4A;
  --color-accent: #2E7D9B;
  --color-positive: #1A6B42;
  --color-neutral: #5C6B7A;
  --color-caution: #8B5E00;
  --color-surface: #F5F7FA;
  --color-divider: #D0D7E0;
  --color-text: #1C2430;
  --color-text-muted: #6B7685;
  --font-heading: Inter, sans-serif;
  --font-body: Inter, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
}
```

---

## Aplicação programática

`scripts/generate_executive_xls.py` aplica:
- header fill #1B2A4A com texto branco
- linhas alternadas #F5F7FA / branco
- borda #D0D7E0 thin
- fonte Inter 10pt
- altura de linha 18pt

Fonts não embutidas no openpyxl: o XLSX referencia "Inter" por nome.
Em sistemas sem Inter instalada, o fallback do leitor (Excel, Google
Sheets) aplica Calibri.

## Validação

Gate G4 (via validate_qa.py) verifica:
- D13: header da A-OPS usa #1B2A4A com texto branco.
- D14: A-FINAL aplica margens A4 (top 25mm, bottom 20mm, left 25mm,
  right 20mm) — ou marca explicitamente "design override applied".
- D15: tipografia respeita Inter (heading 600 / body 400) ou
  fallback declarado.
