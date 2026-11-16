{
  "enableArtifact": false,
  "skillOverrides": {
    "artifact-design": "off",
    "artifact-diagramming": "off",
    "artifact-capabilities": "off",
    "anthropic-skills:docs": "off"
  },
  "env": {
    "CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH": "1",
    "CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS": "5"
  },
  "permissions": {
    "defaultMode": "default",
    "allow": [
      "WebSearch",
      "Bash(git status *)",
      "Bash(git diff *)",
      "Bash(git log *)",
      "Bash(git show *)",
      "Bash(<TEST-BEFEHL> *)",
      "Bash(<TYPECHECK-BEFEHL> *)",
      "Bash(<LINT-BEFEHL> *)",
      "PowerShell(git status *)",
      "PowerShell(git diff *)",
      "PowerShell(git log *)",
      "PowerShell(git show *)",
      "PowerShell(<TEST-BEFEHL> *)",
      "PowerShell(<TYPECHECK-BEFEHL> *)",
      "PowerShell(<LINT-BEFEHL> *)"
    ],
    "ask": [
      "Bash(git commit *)",
      "PowerShell(git commit *)",
      "WebFetch"
    ],
    "deny": [
      "Agent",
      "Workflow",
      "Agent(general-purpose)",
      "Artifact",
      "mcp__claude_ai_Claude_Docs__*",
      "Bash(rm *)",
      "Bash(sudo *)",
      "Bash(git push *)",
      "Bash(git reset --hard *)",
      "Bash(git clean *)",
      "Bash(git -C * push *)",
      "Bash(git -C * reset --hard *)",
      "Bash(git -C * clean *)",
      "PowerShell(Remove-Item *)",
      "PowerShell(rm *)",
      "PowerShell(del *)",
      "PowerShell(git push *)",
      "PowerShell(git reset --hard *)",
      "PowerShell(git clean *)",
      "PowerShell(git -C * push *)",
      "PowerShell(git -C * reset --hard *)",
      "PowerShell(git -C * clean *)",
      "Read(.env)",
      "Read(.env.*)",
      "Read(secrets/**)",
      "Read(**/*.pem)",
      "Read(**/*.key)"
    ]
  },
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|clear|resume",
        "hooks": [
          {
            "type": "command",
            "command": "powershell.exe",
            "args": ["-NoProfile", "-Command", "$f = Get-ChildItem -Name -File -Path (Join-Path $env:CLAUDE_PROJECT_DIR 'uebergabe') -Filter '*.md' -ErrorAction SilentlyContinue | Where-Object { $_ -ne '_vorlage.md' }; if ($f) { 'Offene Uebergaben in uebergabe/: ' + ($f -join ', ') }; exit 0"]
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "powershell.exe",
            "args": ["-NoProfile", "-ExecutionPolicy", "Bypass", "-File", "${CLAUDE_PROJECT_DIR}/.claude/hooks/kennungen.ps1"],
            "timeout": 30,
            "statusMessage": "Kennungen im Bestand suchen"
          }
        ]
      }
    ]
  }
}
