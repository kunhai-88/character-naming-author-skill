# Contributing

感谢你改进作者式角色取名方法。项目欢迎规则修正、匿名化失败案例、命名制度、文档和检查脚本贡献。

## 开始之前

1. 搜索现有 Issues，避免重复讨论。
2. 较大的方法变更先开 Issue，说明它解决的具体失败案例。
3. 不要提交未获授权的剧本、真实人物资料、聊天记录或可识别个人信息。

## 本地验证

```bash
python3 skill/scripts/install_voice_dependency.py
python3 -m unittest discover -s tests -v
python3 scripts/validate_skill.py
python3 scripts/validate_benchmarks.py
python3 scripts/package_skill.py
```

所有命令均应在仓库根目录运行。核心脚本保持标准库兼容；安装器会把 `skill/requirements-voice.txt` 中固定的可选依赖放进 Skill 自己的 `.voice-venv`，不修改系统 Python。

## 修改原则

- `skill/SKILL.md` 保持简洁，只放运行工作流；
- 详细方法放入 `skill/references/`，避免重复；
- 确定性、可重复的检查放入 `skill/scripts/`；
- 不把高频字提示扩张成机械禁用词表；
- 每条新规则必须能对应一个明确失败模式；
- 主角名必须同时验证真实性、复述性与剧情占有，不接受只降低 AI 味的改动；
- 新的定性边界应添加匿名化 regression case，但不得声称自动化脚本能判断文学质量；
- 新增脚本行为必须补充测试。
- 语音规则必须输出可解释信号，不能把拼音相似度包装成文学评分；
- 盲测工具不得默认上传候选、剧本或测试者信息。

## Pull Request

PR 应说明：

- 发现了什么问题；
- 为什么现有规则无法处理；
- 修改会怎样影响用户；
- 使用了哪些匿名化测试案例；
- 本地验证结果。

维护者可能要求拆分范围过大的 PR。提交贡献即表示你同意以项目 MIT License 发布该贡献。
