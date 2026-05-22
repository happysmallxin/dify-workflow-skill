# 常见坑

| 问题 | 原因 | 解决 |
|------|------|------|
| `KeyError: 'workflow'` | 结构路径错误 | 路径是 `['workflow']['graph']`，非 `['app']['workflow']` |
| edge 引用失效 | 删节点未同步删边 | 先删边再删节点 |
| replace 不生效 | PyYAML dump 后换行符变化 | 用更短匹配串或分步替换 |
| SQL 输出为空 | output_format 不是 json | 检查 `tool_configurations.output_format.value` |
| 导入失败 | YAML 结构不完整 | `yaml.safe_load` 先验证 |
| UNION collation 冲突 | 两表字段 collation 不同 | 加 `COLLATE utf8mb4_unicode_ci` 统一，**必须加 `AS 别名`** |
| `int(None)` TypeError | `.get(key, default)` 对 None 值无效 | 用 `int(r.get('key') or 0)` |
| Code 节点运行时崩溃 | 输入可能为 None/字符串而非 list | 加类型检查：`isinstance(data, list)` |
| 导入后名称覆盖 | 同名应用冲突 | 导入前自动加 `_MMdd_HHmm` 时间戳后缀 |
| LLM 输出乱码 | prompt 中的 emoji 不被沙箱支持 | 用纯文本替代 emoji |
