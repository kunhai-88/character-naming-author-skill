# Character Naming Author Skill

[![CI](https://github.com/kunhai-88/character-naming-author-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/kunhai-88/character-naming-author-skill/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/kunhai-88/character-naming-author-skill?display_name=tag)](https://github.com/kunhai-88/character-naming-author-skill/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skill](https://img.shields.io/badge/Agent-Skill-5b5bd6)](skill/SKILL.md)

[English](README.en.md) | 简体中文

一个面向中文短剧、影视剧、小说、AI 漫剧和原创故事的作者式角色取名 Skill。

它不把“坚韧、温柔、深沉”等人物标签拼成漂亮名字，也不把“普通”误当作高级。候选先经过不带解释的裸名门，排除误听、作者短语和解释依赖；通过后才还原人物的出生与取名现场，并用关系和关键场面让名字被剧情占有。

## 它解决什么问题

- 主角名字像批量生成的网文名；
- 名字直接预告人物性格、能力或结局；
- 现实题材人物姓名过于精致、悬浮；
- 整部剧的角色名都像来自同一个取名网站；
- 亲属、同事和对手的名字在成片里听不清、容易混；
- 古装、仙侠人物只有“古风字”，没有宗族、排行、法号或师门制度；
- 需要审查现有角色名，而不是无差别重命名。

## 核心方法

```text
先读故事
→ 信息不足时只追问一个关键事实
→ 生成候选并隐藏全部解释
→ 裸看、裸听，淘汰误听与解释依赖
→ 还原剧中取名者
→ 确定年代、地域、阶层和家庭来源
→ 建立真实姓名带宽
→ 找到一个生活来源的干净异常点
→ 放回四种人物关系中试演
→ 设计名字的首次出现、关系变调与结尾回收
→ 隐藏寓意做两两盲选
→ 只交付一个首选和必要的备选
```

好名字先通过“裸名门”，再通过五关：

- **裸名门**：不看人物解释仍像姓名、听得清、复述得出，不会稳定误听成负面词。

1. **出生关**：人物的父母真可能在那个时间地点取出它；
2. **开口关**：长辈、爱人、对手和陌生人都能自然叫出口；
3. **辨认关**：只听声音也能与同剧人物分开；
4. **复述关**：合上人物表十分钟后仍能说出；
5. **占有关**：经过关系和剧情后逐渐只属于这个人物。

## 安装

### 下载 Release（推荐）

从 [Releases](https://github.com/kunhai-88/character-naming-author-skill/releases) 下载最新的 `character-naming-author.skill`，解压后安装到 Agent Skills 目录。

### 从源码安装

将 `skill/` 目录复制到支持 `SKILL.md` 的 Agent Skills 目录中。例如 Codex：

```bash
cp -R skill ~/.codex/skills/character-naming-author
```

重新启动或刷新 Agent 会话后，在角色取名、整剧姓名审查、反 AI 味改名等任务中触发该 Skill。

## 快速使用

你可以直接提出：

```text
审查这部现实短剧的整套人物名。不要批量换名，先判断哪些应该保留。
```

```text
这个主角名太像网文生成器。请根据人物出生年份、家庭和剧中称呼重新取名。
```

```text
为这个仙侠宗门建立俗名、排行、道号和称呼制度，再决定主角叫什么。
```

建议同时提供人物出生年份、地域、家庭出身、取名者、关键关系和至少一段冲突对白。材料不全时，Skill 会指出哪个事实会实质改变名字，而不是用漂亮字义掩盖猜测。

如果只提供题材而没有人物事实，Skill 会先追问一个关键问题，不再直接生成姓名并倒编出身故事。

Skill 支持单角色新取名、现有名字修复、整剧姓名系统和历史/地域校准四种模式。完整推理在内部执行，默认只交付一个首选、来源、称呼系统、试演和最大风险，避免把用户淹没在候选清单里。

完整示例见 [快速示例](examples/quickstart.md)。

## 确定性检查工具

附带的检查脚本只提示机械风险，不替代文学判断：

```bash
python3 skill/scripts/name_audit.py 叶知意 陆沉川 陆安然 乔若薇
```

JSON 输出：

```bash
python3 skill/scripts/name_audit.py 叶知意 陆沉川 --json
```

它会提示：

- 姓名重复；
- 核心角色同姓但关系未说明；
- 名字共享字或尾字；
- 疑似高频类型化组合。

提示项不是禁用词表。最终判断必须回到人物、家庭和对白。

### 普通话语音检查

安装可选依赖：

```bash
python3 skill/scripts/install_voice_dependency.py
```

检查同音、声母、韵母、声调和声音轮廓碰撞：

```bash
python3 skill/scripts/voice_audit.py 章宁 张凝 赵建军 梁二
```

多音字或特殊读音必须人工覆盖：

```bash
python3 skill/scripts/voice_audit.py 单超 山超 --pronunciation 单超=shan4,chao1
```

语音工具使用 [pypinyin](https://pypi.org/project/pypinyin/)，只提示普通话听觉风险，不替代方言、演员朗读和文学判断。

### 本地人类盲测

```bash
python3 skill/scripts/blind_test.py prepare examples/blind-test-input.json work/blind-session.json --seed 7
python3 skill/scripts/blind_test.py record work/blind-session.json work/feedback.jsonl \
  --winner A --most-real A --most-memorable B --most-owned A \
  --recalled-name 曹晓琴 --reason-code memorable_real
```

盲测会随机候选并删除解释。反馈只写入用户指定的本地 JSONL，不进行网络上传。

## 目录

```text
skill/
├── SKILL.md
├── references/
│   ├── author-naming-method.md
│   ├── anti-ai-audit.md
│   ├── memorability-and-ownership.md
│   ├── candidate-selection.md
│   ├── reality-calibration.md
│   ├── naming-mechanism-library.md
│   └── human-evaluation.md
├── requirements-voice.txt
└── scripts/
    ├── name_audit.py
    ├── voice_audit.py
    ├── install_voice_dependency.py
    └── blind_test.py
tests/
├── test_name_audit.py
├── test_voice_audit.py
├── test_install_voice_dependency.py
└── test_blind_test.py
benchmarks/
├── README.md
└── regression_cases.json
scripts/
├── validate_skill.py
├── validate_benchmarks.py
└── package_skill.py
```

## 开发与验证

核心 Skill 使用 Python 标准库，建议 Python 3.10 或更高版本。普通话语音检查额外使用固定版本的 `pypinyin`。

```bash
python3 skill/scripts/install_voice_dependency.py
python3 -m unittest discover -s tests -v
python3 scripts/validate_skill.py
python3 scripts/validate_benchmarks.py
python3 scripts/package_skill.py
```

打包产物位于 `dist/character-naming-author.skill`。CI 会在 Python 3.10—3.13 上运行测试、验证 Skill 结构与定性回归案例，并生成安装包。

## 设计边界

- 检查脚本只发现机械风险，不对文学质量自动打分；
- 高频字是复核提示，不是禁用词；
- 时代与地域姓名判断需要可靠人物背景，不能靠模型臆测；
- 本项目不会收集或上传用户剧本；
- 好名字无法脱离故事、家庭和称呼关系单独成立。
- “真实但能搬进十部剧”的主角名仍会被淘汰；
- 定性 benchmark 固化重要判断边界，但不伪装成文学质量自动评分器。
- 普通话拼音检查不能替代方言与真人围读，多音字必须确认实际读法；
- 人类盲测用于校准，不把单次选择自动外推成稳定审美。

## 贡献

欢迎提交真实但已匿名化的失败案例、命名制度、规则修正和脚本改进。开始前请阅读 [贡献指南](CONTRIBUTING.md) 与 [行为准则](CODE_OF_CONDUCT.md)。安全问题请按照 [安全政策](SECURITY.md) 私下报告。

版本变化记录在 [CHANGELOG](CHANGELOG.md)。

## 隐私说明

仓库不包含私有剧本、人物资料或本地测试报告。示例姓名仅用于说明常见的类型化命名风险。

## License

[MIT](LICENSE)
