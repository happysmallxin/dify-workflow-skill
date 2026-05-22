---
name: dify-workflow
description: Modify Dify workflow YAML files (DSL format) — add/remove/update nodes, edges, code, LLM prompts — and import into Dify via API. Use when the user says "修改 Dify YAML", "更新工作流", "导入 Dify", "dify yml", or references .yml files with Dify workflow structure.
---

# Dify Workflow YAML 修改与导入

## 前置

```bash
python3 -c "import yaml; print('OK')" 2>/dev/null || pip3 install pyyaml --break-system-packages
```

## YAML 结构

```yaml
app: {description, icon, mode, name, ...}
workflow:
  graph:
    edges: [...]     # 连线
    nodes: [...]     # 节点
    viewport: {...}
```

操作路径：`data['workflow']['graph']['edges']` / `data['workflow']['graph']['nodes']`

## 动态时间参数

**所有 SQL 节点统一用动态时间，禁止硬编码日期。**

| 参数 | 含义 | SQL 写法 |
|------|------|---------|
| `{{#time_node.start_time#}}` | 本期起始 | `date >= '{{#time_node.start_time#}}'` |
| `{{#time_node.end_time#}}` | 本期结束 | `date < '{{#time_node.end_time#}}'` |
| `{{#time_node.prev_start_time#}}` | 上期起始 | 同上 |
| `{{#time_node.prev_end_time#}}` | 上期结束 | 同上 |

**禁止** `DATE() = CURDATE()`、`TO_DAYS() = TO_DAYS(NOW())` 等硬编码。

## 通用修改脚本模板

```python
import yaml

filepath = 'workflow.yml'
with open(filepath, 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)

g = data['workflow']['graph']

# 1. 删除边
g['edges'] = [e for e in g['edges'] if e['id'] not in {'edge_id_1', 'edge_id_2'}]

# 2. 删除节点
g['nodes'] = [n for n in g['nodes'] if n['id'] not in {'node_id_1', 'node_id_2'}]

# 3. 添加节点和边
g['nodes'].append(new_node_dict)
g['edges'].append(new_edge_dict)

# 4. 修改已有节点
for n in g['nodes']:
    if n['id'] == 'target_id':
        n['data']['code'] = 'new code...'
        n['data']['variables'] = [...]

# 5. 写回
with open(filepath, 'w', encoding='utf-8') as f:
    yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)
```

## 节点类型

完整参考见 `references/node-types.md`，包含 SQL 查询节点、Code 节点、LLM 节点的完整 Python 字典模板。

关键注意点：
- Code 节点：`value_selector[0]` 是上游节点 ID，`value_selector[1]` 是输出字段名，函数签名参数数 = variables 长度
- SQL 节点：`tool_configurations.output_format.value` 建议为 `json`
- Edge 结构参考 `references/edge-structure.md`

## 常见操作清单

### 替换 SQL 查询链
1. 删除旧 tool 节点 + 下游 code formatter 节点
2. 删除相关 edges
3. 创建新 tool 节点
4. 添加 edges：上游 → new_tool → downstream_code
5. 更新 downstream_code 的 variables 和 code
6. 更新下游 LLM prompt_template 中的旧指标名称
7. 全局搜索旧节点 ID/旧指标名确认无残留

### 修改 table_merge
- variables 顺序决定函数 arg1, arg2...
- 代码中必须处理 None、空字符串、非标准 JSON
- 输出 result (markdown) 和 data_json (JSON string)

### 更新 LLM 提示词
```python
for pt in node['data']['prompt_template']:
    pt['text'] = pt['text'].replace('旧文本', '新文本')
```

### 修改 SQL 日期为动态参数
```sql
col >= '{{#time_node.start_time#}}' AND col < '{{#time_node.end_time#}}'
```

## 验证 Checklist
- [ ] `yaml.safe_load()` 正常解析
- [ ] 每个 edge source/target 在 nodes 中存在
- [ ] 删除的 ID 不在任何 `value_selector`/`{{#...#}}` 中
- [ ] 新 ID 唯一
- [ ] SQL 使用动态时间参数，无硬编码
- [ ] Code 函数参数数 = variables 长度
- [ ] `sourceType`/`targetType` 匹配实际节点 type
- [ ] 全局搜索旧指标名称/ID 确认无残留
- [ ] **所有 Code 节点代码能通过 `compile()` 编译**
- [ ] **Code 节点函数本地测试通过（含 None/空输入边界测试）**
- [ ] **所有 SQL 节点通过 MCP MySQL 验证**

## 导入前验证

### Code 节点验证

运行 `scripts/verify_code_nodes.py <yml_file>` 对所有 Code 节点进行编译检查和边界测试。

### SQL 节点验证

运行 `scripts/verify_sql_nodes.py <yml_file>` 提取所有 SQL。然后通过 MCP MySQL 逐条执行验证。

常见 Code 节点坑：
- `int(None)` → TypeError，用 `int(r.get('key') or 0)` 而非 `int(r.get('key', 0))`
- `.get(key, default)` 只在 key 不存在时返回 default，key 存在但值为 None 时返回 None
- f-string 中避免 emoji，Dify 沙箱可能不支持
- 输入参数可能是 None/string/list，需要类型检查

## 导入 Dify

**导入前必须自动在应用名称后追加时间戳后缀**，格式为 `_MMdd_HHmm`，避免同名覆盖。

```bash
YAML_FILE="workflow.yml"
python3 -c "
import json, yaml
from datetime import datetime

with open('$YAML_FILE', 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)

ts = datetime.now().strftime('%m%d_%H%M')
data['app']['name'] = f\"{data['app']['name']}_{ts}\"

yaml_str = yaml.dump(data, allow_unicode=True, default_flow_style=False, sort_keys=False)
payload = json.dumps({'mode': 'yaml-content', 'yaml_content': yaml_str}, ensure_ascii=False)
with open('/tmp/dify_import.json', 'w', encoding='utf-8') as f:
    f.write(payload)
print(f\"App name: {data['app']['name']}\")
"
curl -s -k -X POST "https://10.1.2.111:80/console/api/apps/imports" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d @/tmp/dify_import.json
```

## 常见坑

详见 `references/common-pitfalls.md`
