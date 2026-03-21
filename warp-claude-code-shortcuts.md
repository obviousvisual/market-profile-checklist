# Warp Terminal + Claude Code: Keyboard Shortcuts Cheatsheet

## Part 1: Essential Claude Code Shortcuts

### The "Must Know" Basics

| Shortcut | What it does | When you'll use it |
|----------|-------------|-------------------|
| `Ctrl+C` | Cancel current generation | When Claude is going down the wrong path |
| `Ctrl+D` | Exit Claude Code | Done for the day |
| `Escape` `Escape` | Rewind / undo last action | Claude broke something, go back |
| `Ctrl+L` | Clear screen (keeps conversation) | Screen clutter |
| `Up/Down arrows` | Scroll through your previous prompts | Re-send or tweak a prompt |
| `Tab` | Accept autocomplete suggestion | File paths, commands |
| `Shift+Tab` | Toggle permission modes | Switch between Auto-Accept / Plan Mode / Normal |

### Multiline Input (writing longer prompts)

| Shortcut | Context |
|----------|---------|
| `\` then `Enter` | Works everywhere |
| `Ctrl+J` | Line feed (all terminals) |
| `Shift+Enter` | Works in Warp |

### Editing Your Prompt

| Shortcut | What it does |
|----------|-------------|
| `Ctrl+G` | Open prompt in external text editor |
| `Ctrl+K` | Delete from cursor to end of line |
| `Ctrl+U` | Delete entire line |
| `Ctrl+Y` | Paste last deleted text |
| `Alt+B` / `Alt+F` | Jump back/forward one word |

### Useful Toggles

| Shortcut | What it does |
|----------|-------------|
| `Alt+T` | Toggle extended thinking on/off |
| `Alt+P` | Switch model without clearing prompt |
| `Ctrl+O` | Toggle verbose output |
| `Ctrl+T` | Toggle task list visibility |
| `Ctrl+R` | Reverse-search your prompt history |

### Most-Used Slash Commands

| Command | What it does |
|---------|-------------|
| `/help` | Show help |
| `/clear` | Start fresh session |
| `/compact` | Summarize conversation (free up context) |
| `/commit` | Create a git commit |
| `/model` | Switch AI models |
| `/vim` | Toggle vim-style editing |
| `/memory` | View/edit CLAUDE.md memory files |
| `/cost` | Check token usage and costs |
| `/resume` | Resume a previous session |
| `/keybindings` | Customize keyboard shortcuts |

### Quick Input Prefixes

| Prefix | What it does |
|--------|-------------|
| `/` | Access commands and skills |
| `!` | Run a bash command directly |
| `@` | Autocomplete a file path to attach |

---

## Part 2: Setting Up Shortcuts in Warp Terminal

### Option A: Settings UI (Easiest)

1. Open Warp
2. Go to **Settings > Keyboard Shortcuts** (or press `Cmd+,` / `Ctrl+,`)
3. Search for the action you want to rebind
4. Click and type your new shortcut
5. Conflicts are highlighted with an orange border

Press **Cmd+/** (macOS) or **Ctrl+/** (Linux) to view all current shortcuts in a side panel.

### Option B: YAML Config File (More Control)

Warp stores keybindings in a YAML file:

- **macOS/Linux:** `~/.warp/keybindings.yaml`
- **Windows:** `$env:LOCALAPPDATA\warp\Warp\config\keybindings.yaml`

Create the directory if it doesn't exist:

```bash
mkdir -p ~/.warp
```

Example `keybindings.yaml` entries:

```yaml
# Example: Custom keybindings for Warp
# Format varies by action - see Warp docs for full action list
```

After saving, restart Warp to pick up changes.

### Option C: Community Presets

Download ready-made keybinding sets from:
- [warpdotdev/keysets](https://github.com/warpdotdev/keysets) (official presets)

Copy the `.yaml` file into `~/.warp/` and restart Warp.

### Warp's Built-in Shortcuts Worth Knowing

| Shortcut | What it does |
|----------|-------------|
| `Ctrl+Shift+T` | New tab |
| `Ctrl+Shift+N` | New window |
| `Ctrl+R` | Search command history (Warp's own) |
| `Ctrl+Shift+L` | Open Warp AI |
| `Ctrl+/` | Show all keyboard shortcuts |

### Tips for Avoiding Conflicts

- Warp and Claude Code both run in the same terminal, so **Ctrl+R**, **Ctrl+L**, and **Ctrl+C** are shared
- When Claude Code is active, Claude Code captures these keys
- When you're at the normal Warp prompt (Claude not running), Warp handles them
- If you remap Warp shortcuts, avoid overriding `Ctrl+C`, `Ctrl+D` (reserved by Claude Code)

---

## Quick Reference Card

```
DAILY WORKFLOW:
  Start Claude:     claude
  Cancel output:    Ctrl+C
  Undo last action: Esc Esc
  New line:         \ + Enter  or  Shift+Enter
  Clear screen:     Ctrl+L
  Save context:     /compact
  Commit work:      /commit
  Exit:             Ctrl+D

POWER USER:
  Toggle thinking:  Alt+T
  Switch model:     Alt+P
  Search history:   Ctrl+R
  Attach file:      @filename
  Run bash:         !command
  Edit in editor:   Ctrl+G
```

---

Sources:
- [Warp Keyboard Shortcuts Docs](https://docs.warp.dev/getting-started/keyboard-shortcuts)
- [Warp Custom Keysets Repo](https://github.com/warpdotdev/keysets)
- [Warp Customization Guide](https://docs.warp.dev/getting-started/readme-1/customizing-warp)
- [Claude Code Keybindings Docs](https://docs.anthropic.com/en/docs/claude-code/keybindings)
