# Character Naming Author Skill

[![CI](https://github.com/kunhai-88/character-naming-author-skill/actions/workflows/ci.yml/badge.svg)](https://github.com/kunhai-88/character-naming-author-skill/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/kunhai-88/character-naming-author-skill?display_name=tag)](https://github.com/kunhai-88/character-naming-author-skill/releases)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

English | [简体中文](README.md)

An Agent Skill for naming and auditing characters in Chinese short dramas, screenplays, fiction, and AI-generated drama projects.

Instead of assembling attractive characters from personality labels—or treating bland realism as literary quality—the Skill reconstructs the naming situation, adds one life-derived point of distinction, and lets relationships and scenes make the name memorable.

## What it does

- audits a complete cast before renaming anyone;
- detects names that announce personality, power, or destiny;
- reconstructs period, region, class, family, and naming authority;
- distinguishes legal names, childhood names, aliases, titles, and religious names;
- tests names in intimate, everyday, adversarial, and formal dialogue;
- tests unaided recall and resistance to being transplanted into unrelated stories;
- designs public, private, formal, and adversarial forms of address;
- calibrates period and regional plausibility with public, privacy-respecting name neighborhoods when needed;
- plans the first use, relational change, and final narrative return of a name;
- reviews the result without relying on symbolic explanations;
- flags mechanical collisions with a deterministic Python tool.

## Install

Download `character-naming-author.skill` from [Releases](https://github.com/kunhai-88/character-naming-author-skill/releases), or copy the source directory:

```bash
cp -R skill ~/.codex/skills/character-naming-author
```

Restart or refresh the Agent session after installation.

## Example requests

```text
Audit the names in this Chinese family drama. Preserve names that already work.
```

```text
This protagonist's name feels machine-generated. Rename them from their birth year, family, region, and dialogue.
```

The method and output are written primarily for Chinese-language character naming. See [the quick example](examples/quickstart.md) for an anonymized walkthrough.

## Development

Python 3.10+ is recommended. The project uses only the standard library.

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_skill.py
python3 scripts/validate_benchmarks.py
python3 scripts/package_skill.py
```

## Limits

- The script flags mechanical risks; it does not score literary quality.
- Frequent characters are review hints, not forbidden words.
- Period and regional judgments require reliable character context.
- The project does not collect or upload user manuscripts.

See [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), and the [MIT License](LICENSE).
