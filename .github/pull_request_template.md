## What changed

<!-- 概述本 PR 的范围。 -->

## Why

<!-- 描述现有方法的具体失败场景。请使用匿名化材料。 -->

## Validation

- [ ] `python3 -m pip install -r skill/requirements-voice.txt`
- [ ] `python3 -m unittest discover -s tests -v`
- [ ] `python3 scripts/validate_skill.py`
- [ ] `python3 scripts/validate_benchmarks.py`
- [ ] `python3 scripts/package_skill.py`
- [ ] 未包含私人剧本、个人信息、本机绝对路径或凭据
- [ ] 新规则对应明确失败模式，而非扩大禁用词表
- [ ] 盲测与反馈数据保持本地，公开案例已经匿名化

## User impact

<!-- 说明这会怎样改变 Skill 的行为和输出。 -->
