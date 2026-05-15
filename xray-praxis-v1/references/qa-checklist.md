# PRAXIS — QA Checklist (Gate G4)

Lista de verificação programática executada por `scripts/validate_qa.py`
antes do release final na Fase 6. Total: 18 checagens.

Cada item retorna PASS ou FAIL. Qualquer FAIL bloqueia G4.

## Bloco A: integridade do caso

A1. manifest.yaml existe e parseia como YAML válido.
A2. case_id segue o formato praxis-YYYYMMDD-XXXXXXXX.
A3. current_phase ∈ {1, 2, 3, 4, 5, 6}.
A4. Cada item de artifacts_produced[] referencia um arquivo que existe em disco.

## Bloco B: epistemic compliance

B5. Todo artefato com `epistemic_required: true` no registry contém ao
    menos uma ocorrência de [FATO], [INFERÊNCIA] ou [HIPÓTESE].
B6. A-MASTER contém ao menos UMA ocorrência de [FATO] (regra C7 do
    Agente 00).
B7. Em A-FINAL, NENHUMA das strings cruas [FATO], [INFERÊNCIA] ou
    [HIPÓTESE] aparece no texto exibido ao cliente.
B8. Em A-FINAL, NENHUMA ocorrência de [TRILHA_INTERNA] permanece.

## Bloco C: voice compliance

C9.  Em deliverables de cliente (A-02, A-03, A-04, A-FINAL), zero
     ocorrências das frases proibidas: "Claro!", "Vamos lá!", "Com
     certeza!", "Como IA", "Sou um modelo", "ChatGPT", "Claude", "GPT".
C10. Em deliverables de cliente, zero emojis (range Unicode 1F300–1FAFF
     e 2600–27BF).
C11. Cabeçalho do consultor presente no topo de cada deliverable de
     cliente (logo OU display name).
C12. Bloco de assinatura presente no rodapé de cada deliverable de
     cliente.

## Bloco D: design system compliance

D13. A-OPS (xlsx) usa header fill #1B2A4A com texto branco.
D14. A-FINAL aplica margens A4 conforme design-system.md (top 25mm,
     bottom 20mm, left 25mm, right 20mm) — ou marca explicitamente
     "design override applied".
D15. Tipografia respeita Inter (heading 600 / body 400) ou fallback
     declarado.

## Bloco E: completude do plano de ação

E16. A-MASTER seção 5 contém ao menos um item de ação com:
     - frase imperativa
     - prazo concreto
     - responsável (nomeado ou [A DEFINIR])
     - KPI/indicador
E17. Próximos passos na seção 6 estão sincronizados com a seção 5
     (sem itens órfãos).

## Bloco F: governança

F18. gates_passed[] inclui G0, G1, G2, G3 antes de G4 ser avaliado.
     (Cenários B e C aplicam regras especiais — ver scenario-router.md.)

## Output esperado de validate_qa.py

Saída padrão:
```
QA Report — case_id=praxis-YYYYMMDD-XXXXXXXX
Total checks: 18
Passed: N
Failed: N
Issues:
  - [check_id] description of failure
```

Exit code 0 se todos passarem; 1 caso contrário.

## Política de exceção

O consultor pode marcar uma checagem como `WAIVED` em manifest.yaml
sob `qa_waivers:`. O sistema registra a exceção mas permite o avanço.
Toda exceção é listada explicitamente em A-MASTER Apêndice A.

Exceções proibidas: B6, B7, B8, C9, C10. Estas não admitem waiver.
