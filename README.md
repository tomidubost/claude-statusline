# claude-statusline

Status line para [Claude Code](https://claude.com/claude-code) que muestra:

- **Línea 1:** modelo actual · rama de git (funciona también en worktrees)
- **Línea 2:** uso del contexto · límite de 5 h con hora de reinicio y tiempo restante · costo de la sesión en USD

Las barras cambian de color según el uso: verde < 50 %, amarillo < 80 %, rojo ≥ 80 %.

## Requisitos

- Claude Code
- `python3` en el PATH (sin dependencias extra)

## Instalación rápida

```bash
curl -fsSL https://raw.githubusercontent.com/tomidubost/claude-statusline/main/install.sh | bash
```

Descarga el script a `~/.claude/statusline-tokens.py` y agrega la entrada `statusLine` a `~/.claude/settings.json` sin tocar el resto (deja un respaldo en `settings.json.bak`). Después reinicia Claude Code.

## Instalación manual

1. Copia el script:

   ```bash
   curl -fsSL https://raw.githubusercontent.com/tomidubost/claude-statusline/main/statusline-tokens.py -o ~/.claude/statusline-tokens.py
   chmod +x ~/.claude/statusline-tokens.py
   ```

2. Agrega esto a `~/.claude/settings.json`:

   ```json
   "statusLine": {
     "type": "command",
     "command": "~/.claude/statusline-tokens.py",
     "refreshInterval": 30
   }
   ```

3. Reinicia Claude Code.

## Desinstalar

Borra la clave `statusLine` de `~/.claude/settings.json` y el archivo `~/.claude/statusline-tokens.py`.
