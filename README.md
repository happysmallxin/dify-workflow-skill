# Dify Workflow Skill

A Claude Code skill for modifying Dify workflow YAML files (DSL format) and importing them into Dify via API.

## Features

- **YAML Structure Manipulation**: Add, remove, and update nodes, edges, code, and LLM prompts in Dify DSL files
- **SQL Query Management**: Create and modify SQL query nodes with dynamic time parameters
- **Code Node Validation**: Pre-import validation of all Code nodes (compile checks + boundary tests)
- **SQL Verification**: MCP-based SQL syntax verification before import
- **Auto-import**: One-command import to Dify with automatic timestamp naming

## Installation

### Via Claude Code Plugin

```bash
# Clone the repository
git clone https://github.com/happysmallxin/dify-workflow-skill.git

# Install as local skill
claude plugins install /path/to/dify-workflow-skill
```

### Manual Installation

Copy the skill directory to your Claude Code skills folder:

```bash
cp -r dify-workflow-skill ~/.claude/skills/dify-workflow/
```

## Prerequisites

- Python 3 with `pyyaml`: `pip3 install pyyaml`
- Access to a Dify instance with Console API token
- (Optional) MCP MySQL connection for SQL verification

## Usage

Once installed, the skill activates when you:
- Say "修改 Dify YAML" / "更新工作流" / "导入 Dify" / "dify yml"
- Reference `.yml` files with Dify workflow structure

### Key Workflows

1. **Modify workflow**: Edit nodes, edges, SQL queries, LLM prompts
2. **Pre-import validation**: All Code nodes are compiled and tested, all SQL nodes are verified via MCP
3. **Import to Dify**: Automatic timestamp suffix + API import

## Structure

```
dify-workflow-skill/
├── .claude-plugin/
│   └── plugin.json          # Skill manifest
├── skills/
│   └── dify-workflow/
│       └── SKILL.md          # Core skill knowledge
├── references/
│   ├── node-types.md         # SQL/Code/LLM node templates
│   ├── edge-structure.md     # Edge structure reference
│   └── common-pitfalls.md   # Known issues and solutions
├── scripts/
│   ├── verify_code_nodes.py  # Code node compiler + boundary tests
│   └── verify_sql_nodes.py   # SQL extraction for MCP verification
├── README.md
└── LICENSE
```

## License

MIT
