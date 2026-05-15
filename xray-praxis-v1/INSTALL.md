# INSTALL — PRAXIS v1.0.0

Este guia cobre instalação em três contextos: Claude.ai (web/desktop),
Claude Code (terminal) e via Anthropic API.

---

## Pré-requisitos

- Python 3.10 ou superior.
- Acesso a um cliente Claude (Claude.ai, Claude Code, ou Anthropic API).
- Pacotes Python: `pyyaml`, `openpyxl`.

```bash
pip install pyyaml openpyxl --break-system-packages
```

Em ambientes onde `--break-system-packages` não é necessário ou
recomendado, prefira venv:

```bash
python -m venv .venv
source .venv/bin/activate
pip install pyyaml openpyxl
```

---

## Opção 1 — Claude.ai (web e desktop)

A skill é instalada via interface gráfica:

1. Faça upload de `praxis.zip` na seção de skills das configurações.
2. Aguarde o processamento.
3. Em qualquer conversa, mencione "novo caso PME" ou
   "iniciar consultoria" — a skill será ativada por meio do trigger
   declarado em `SKILL.md`.

Notas:
- A execução de scripts Python ocorre dentro do sandbox de
  computer-use do Claude (quando habilitado).
- Os artefatos gerados ficam disponíveis para download via UI.

---

## Opção 2 — Claude Code (terminal)

1. Copie a pasta `praxis/` para o diretório de skills do Claude Code:

   ```bash
   unzip praxis.zip -d ~/.claude/skills/
   ```

   (caminho padrão; pode variar conforme a configuração local).

2. Verifique a estrutura:

   ```bash
   ls ~/.claude/skills/praxis
   # SKILL.md  README.md  INSTALL.md  BUILD_NOTES.md  references/  agents/
   # scripts/  assets/  schemas/  manifest_template.yaml
   ```

3. Instale as dependências Python:

   ```bash
   pip install pyyaml openpyxl --break-system-packages
   ```

4. Execute o teste de instalação:

   ```bash
   cd ~/.claude/skills/praxis && python scripts/dry_run.py
   ```

   Saída esperada: `RESULT: PASS`.

5. Em uma sessão do Claude Code, inicie um caso:

   ```
   novo caso PME para Cliente Exemplo Ltda
   ```

---

## Opção 3 — Anthropic API

A skill funciona enviando o conteúdo de `SKILL.md` (e referências sob
demanda) como contexto. Padrão sugerido:

```python
import anthropic, pathlib

client = anthropic.Anthropic()

skill_md = pathlib.Path("praxis/SKILL.md").read_text(encoding="utf-8")

system_prompt = (
    "Você é um co-piloto consultivo. Use a skill PRAXIS abaixo "
    "como guia operacional. Leia as referências sob demanda quando "
    "uma fase ativa exigir.\n\n" + skill_md
)

response = client.messages.create(
    model="claude-opus-4-7",
    max_tokens=4096,
    system=system_prompt,
    messages=[
        {"role": "user", "content": "novo caso PME para Cliente Exemplo Ltda"}
    ],
)
print(response.content[0].text)
```

Para que a skill produza artefatos (XLSX, MD), o consumidor da API
precisa expor as ferramentas de execução de código (computer-use,
function-calling) e mapear chamadas a `scripts/*.py` no host.

---

## Verificação pós-instalação

Independente da plataforma, o comando canônico de verificação é:

```bash
cd <praxis_path> && python scripts/dry_run.py
```

Resultado válido:

```
============================================================
RESULT: PASS
All 6 phases executed; QA returned exit 0.
============================================================
```

Em caso de falha, o workdir é mantido em `/tmp/praxis_dryrun_*` para
inspeção.

---

## Atualizações

PRAXIS v1.0.0 não requer migração entre versões (primeira release).
Versões futuras incluirão notas em `BUILD_NOTES.md` quando houver
mudanças de schema (manifest, gates).

---

## Suporte

- Bugs e sugestões: abra issue no repositório (ou canal interno do
  consultor).
- Casos de uso fora dos cenários A/B/C: documente em
  `BUILD_NOTES.md` para evolução posterior.
