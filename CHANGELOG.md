# Changelog

本项目遵循 [Semantic Versioning](https://semver.org/)；版本记录采用 Keep a Changelog 的分类方式。

## [Unreleased]

## [0.3.1] - 2026-07-15

### Fixed

- 新增 Skill 本地隔离环境安装器，避开 macOS/Homebrew Python 的 PEP 668 系统环境限制；
- 语音审计会自动发现 `.voice-venv`，用户无需激活环境或修改系统 Python。

## [0.3.0] - 2026-07-15

### Added

- 12 类作者级正向命名机制库，覆盖排行、辈分、乳名、职业称呼、登记偶然、公私双名、被命名与夺名等来源；
- 基于 `pypinyin 0.55.0` 的普通话声母、韵母、声调、同音与声音相似检查；
- 多音字和特殊姓名读音的人工覆盖；
- 本地匿名盲测准备、随机候选、十分钟回忆记录与 JSONL 反馈汇总；
- 反馈原因码与“跨项目重复后才升级为偏好规则”的校准门禁；
- 语音工具和盲测工具的自动测试与 CI 依赖验证。

### Changed

- 候选生成必须先选择生活机制，不再只从抽象来源卡发散；
- 整剧核心人物超过三人时，增加可解释的普通话声音碰撞检查；
- 用户审美学习从“喜欢哪些字”改为记录失败机制和盲选证据。

## [0.2.0] - 2026-07-15

### Added

- “真实底盘＋一个干净异常点”的正向命名方法；
- 出生、开口、辨认、复述、占有五关门禁；
- 公私称呼系统与名字的首次出现、关系变调、结尾回收设计；
- 候选来源卡、两两盲选、反向替换和十分钟复述测试；
- 基于公开合规样本的年代与地域姓名邻域校准；
- 区分 AI 型、占位型和过度设计型三类失败；
- 六个匿名化定性回归案例及 CI 校验。

### Changed

- 主角名不再以“像真人”为充分条件；可无损迁移的平庸名字必须淘汰；
- 默认输出从字义解释升级为取名现场、记忆来源、称呼系统和剧情占有方案。

## [0.1.0] - 2026-07-15

### Added

- 作者式角色取名工作流；
- 取名方法与反 AI 味盲审参考；
- 姓名机械风险检查脚本及基础测试。

[Unreleased]: https://github.com/kunhai-88/character-naming-author-skill/compare/v0.3.1...HEAD
[0.3.1]: https://github.com/kunhai-88/character-naming-author-skill/compare/v0.3.0...v0.3.1
[0.3.0]: https://github.com/kunhai-88/character-naming-author-skill/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/kunhai-88/character-naming-author-skill/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/kunhai-88/character-naming-author-skill/releases/tag/v0.1.0
