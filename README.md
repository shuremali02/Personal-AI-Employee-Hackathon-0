# Personal AI Employee Hackathon 0 - Foundation Setup

## Project Structure

This project follows the Speckit Plus spec-driven architecture for the Personal AI Employee Hackathon 0. Below is the proper folder structure:

```
personal-ai-employee-hackathon/
├── .claude/                    # Claude Code specific configurations
│   ├── skills/                 # Claude Code skills
│   └── agents/                 # Claude Code agents
├── .specify/                   # Speckit Plus framework files
│   ├── memory/                 # Constitution and persistent memory
│   ├── templates/              # Template files for specs, plans, tasks
│   └── scripts/                # Utility scripts
├── specs/                      # All specifications (this is the main focus)
│   └── 001-foundation-setup/   # Foundation setup specification
│       ├── spec.md             # Feature specification
│       ├── plan.md             # Implementation plan
│       ├── tasks.md            # Implementation tasks
│       ├── research.md         # Research findings
│       ├── data-model.md       # Data models
│       ├── quickstart.md       # Quick start guide
│       ├── contracts/          # API contracts
│       │   └── setup-contracts.yaml
│       └── checklists/         # Quality checklists
│           └── requirements.md
├── history/                    # Project history
│   └── prompts/                # Prompt history records
│       └── 001-foundation-setup/
│           ├── 1-foundation-setup.spec.prompt.md
│           ├── 2-foundation-setup.plan.prompt.md
│           └── 3-foundation-setup.tasks.prompt.md
├── setup-scripts/              # Setup scripts for foundation
├── src/                        # Source code (to be created)
├── tests/                      # Test files (to be created)
├── AI_Employee_Vault/          # Obsidian vault for AI employee
│   ├── Dashboard.md
│   ├── Company_Handbook.md
│   ├── Inbox/
│   ├── Needs_Action/
│   └── Done/
├── .mcp/                       # Model Context Protocol configuration
├── .obsidian/                  # Obsidian configuration
├── .env                        # Environment variables (not committed)
├── .gitignore                  # Git ignore file
├── README.md                   # This file
├── pyproject.toml              # Python project configuration
├── requirements.txt            # Python dependencies
├── package.json                # Node.js dependencies
└── index.js                    # Main entry point
```

## Architecture

The Personal AI Employee follows a modular architecture:

- **Brain**: Claude Code (AI reasoning and decision making)
- **Memory**: Obsidian vault (knowledge storage and retrieval)
- **Senses**: Watchers (email, calendar, file system monitoring)
- **Hands**: MCP servers (external system interaction)

## Prerequisites

- Python 3.13+
- Node.js v24+ LTS
- Claude Code (Pro subscription or Claude Code Router with Free Gemini API)
- Obsidian v1.10.6+
- GitHub Desktop
- uv (Python project manager)

## Important Notes for Setup

### 1. Claude Code Already Installed
If you already have Claude Code installed on your laptop, you can skip the Claude Code installation task (T009) and go directly to verification (T010).

### 2. Obsidian Already Installed
If you already have Obsidian installed, you can proceed with creating the AI_Employee_Vault structure as specified in the tasks.

### 3. UV Package Manager
The project uses `uv` as the Python package manager. If you don't have it installed, run:
```bash
pip install uv
```

### 4. Working Directory
All work should be done in the project root directory (not inside specs/), following the Speckit Plus methodology.

### 5. Security First
- The `.env` file should never be committed to version control
- All sensitive credentials should be stored in the `.env` file
- Make sure `.env` is properly listed in `.gitignore`

## Setup Instructions

1. Ensure you have Claude Code, Obsidian, Python 3.13+, and Node.js v24+ LTS installed
2. Navigate to the project root directory
3. Follow the tasks in `specs/001-foundation-setup/tasks.md` in order
4. Start with the MVP scope: User Story 1 (Development Environment Setup)

## Running Verification

After completing the setup, run the verification script:
```bash
python specs/001-foundation-setup/verify_setup.py
```

## Next Steps

After completing the foundation setup, you'll be ready to proceed with the Bronze tier implementation of your Personal AI Employee.

---

**Note**: This project follows the Personal AI Employee Hackathon 0 Constitution which emphasizes local-first architecture, human-in-the-loop safety, and modular design.