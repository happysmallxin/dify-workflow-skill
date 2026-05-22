# Dify 节点类型完整参考

## SQL 查询节点 (tool / db_query_pre_auth)

```python
{
    'data': {
        'desc': '', 'is_team_authorization': True, 'output_schema': None,
        'paramSchemas': [
            {'auto_generate': None, 'default': None, 'form': 'llm',
             'human_description': {'zh_Hans': 'SQL查询语句，例如：select * from tbl_name', ...},
             'label': {'zh_Hans': 'SQL查询语句', ...},
             'llm_description': '...', 'name': 'query_sql', 'options': [],
             'required': True, 'type': 'string'},
            {'auto_generate': None, 'default': 'markdown', 'form': 'form',
             'human_description': {'zh_Hans': '用于选择输出格式，markdown或json。', ...},
             'label': {'zh_Hans': '输出格式', ...},
             'name': 'output_format',
             'options': [
                 {'value': 'markdown', 'label': {'zh_Hans': 'MARKDOWN', ...}},
                 {'value': 'json', 'label': {'zh_Hans': 'JSON', ...}}
             ],
             'required': True, 'type': 'select'}
        ],
        'params': {'output_format': '', 'query_sql': ''},
        'provider_id': 'junjiem/db_query_pre_auth/db_query_pre_auth',
        'provider_name': 'junjiem/db_query_pre_auth/db_query_pre_auth',
        'provider_type': 'builtin',
        'selected': False,
        'title': '节点标题',
        'tool_configurations': {'output_format': {'type': 'constant', 'value': 'json'}},
        'tool_description': '数据库SQL查询工具（预授权）。',
        'tool_label': 'SQL查询（预授权）',
        'tool_name': 'sql_query_pre_auth',
        'tool_node_version': '2',
        'tool_parameters': {'query_sql': {'type': 'mixed', 'value': 'SELECT ...'}},
        'type': 'tool'
    },
    'height': 89, 'id': 'node_id',
    'position': {'x': 1246, 'y': 331},
    'positionAbsolute': {'x': 1246, 'y': 331},
    'selected': False, 'sourcePosition': 'right', 'targetPosition': 'left',
    'type': 'custom', 'width': 243
}
```

关键配置：
- `tool_configurations.output_format.value`: 建议 `"json"` 确保 Code 节点能解析
- `tool_parameters.query_sql.value`: SQL 语句，使用 `{{#node_id.field#}}` 引用变量

## Code 节点 (type: code)

```python
{
    'data': {
        'code': "import json\n\ndef main(arg1, arg2):\n    ...",
        'code_language': 'python3',
        'desc': '',
        'outputs': {
            'result': {'children': None, 'type': 'string'},
            'data_json': {'children': None, 'type': 'string'}
        },
        'selected': False,
        'title': 'table_merge',
        'type': 'code',
        'variables': [
            {'value_selector': ['upstream_id', 'json'], 'value_type': 'array[object]', 'variable': 'arg1'},
            {'value_selector': ['upstream_id2', 'json'], 'value_type': 'array[object]', 'variable': 'arg2'}
        ]
    },
    'height': 53, 'id': 'code_node_id',
    'position': {'x': 1000, 'y': 500},
    'positionAbsolute': {'x': 1000, 'y': 500},
    'selected': False, 'sourcePosition': 'right', 'targetPosition': 'left',
    'type': 'custom', 'width': 243
}
```

注意：
- `value_selector[0]` 是上游节点 ID，`value_selector[1]` 是输出字段名
- 函数签名参数数必须匹配 variables 数量
- `outputs` 定义返回字段，下游节点通过 `node_id.field` 引用

## LLM 节点 (type: llm)

```python
{
    'data': {
        'context': {'enabled': False, 'variable_selector': []},
        'model': {
            'completion_params': {},
            'mode': 'chat',
            'name': 'qwen3-30b-a3b',
            'provider': 'langgenius/tongyi/tongyi'
        },
        'prompt_template': [
            {'id': 'uuid', 'role': 'system', 'text': '系统提示词...'},
            {'id': 'uuid', 'role': 'user', 'text': '用户提示词... {{#node_id.field#}}'},
            {'id': 'uuid', 'role': 'assistant', 'text': ''}
        ],
        'selected': False, 'title': 'LLM节点', 'type': 'llm',
        'variables': [], 'vision': {'enabled': False}
    },
    'height': 89, 'id': 'llm_node_id',
    'position': {'x': 1500, 'y': 500},
    'positionAbsolute': {'x': 1500, 'y': 500},
    'selected': False, 'sourcePosition': 'right', 'targetPosition': 'left',
    'type': 'custom', 'width': 243
}
```

- `prompt_template` 使用 `{{#node_id.field#}}` 引用上游节点输出
- `model.provider` 常用值：`langgenius/tongyi/tongyi`
- `model.name` 示例：`qwen3-30b-a3b`、`qwen-max-latest`

## Answer 节点、Start 节点、Parameter Extractor、IF/ELSE

详见各节点已有实例，参考模板创建。
