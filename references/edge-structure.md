# Edge 结构参考

## 基本格式

```python
{
    'data': {
        'isInIteration': False,
        'isInLoop': False,
        'sourceType': 'tool',      # 源节点类型: start/tool/code/llm/answer/parameter-extractor/if-else
        'targetType': 'code'       # 目标节点类型
    },
    'id': 'source_id-source-target_id-target',
    'selected': False,
    'source': 'source_id',         # 源节点 ID
    'sourceHandle': 'source',
    'target': 'target_id',         # 目标节点 ID
    'targetHandle': 'target',
    'type': 'custom',
    'zIndex': 0
}
```

## Edge ID 命名规范

格式：`{source_node_id}-source-{target_node_id}-target`

示例：`1778029403849-source-1778031211855-target`

## sourceType/targetType 对照

| 节点 type | sourceType/targetType 值 |
|-----------|--------------------------|
| start | `start` |
| parameter-extractor | `parameter-extractor` |
| tool (SQL) | `tool` |
| code | `code` |
| llm | `llm` |
| answer | `answer` |
| if-else | `if-else` |

**重要**：edge 的 `sourceType`/`targetType` 必须与实际节点 type 匹配，否则 Dify 会报错。
