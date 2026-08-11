# ADR-0003: Adopt Python Development Toolchain

**Status:** Accepted

**Date:** 2026-08-11

## Context

Project Physical AI Partner は Python を主要開発言語として採用する。

本プロジェクトはモノレポ構成を採用し、複数のマイクロサービス（Gateway、Audio、ASR、LLM、Agent、Memory、TTS、Avatar など）を同一リポジトリで管理する。

そのため、すべてのサービスで共通の Python 開発環境・コード品質基準・依存管理方法を採用する必要がある。

---

## Decision

プロジェクト標準の Python 開発ツールチェーンとして以下を採用する。

| Category              | Tool           |
| --------------------- | -------------- |
| Python Version        | Python 3.12    |
| Package Manager       | uv             |
| Project Configuration | pyproject.toml |
| Dependency Lock       | uv.lock        |
| Linter                | Ruff           |
| Formatter             | Ruff Format    |
| Type Checker          | basedpyright   |
| Test Framework        | Pytest         |
| Git Hooks             | pre-commit     |

---

## Alternatives Considered

### pip + venv

**Pros**

* Python標準
* 学習コストが低い

**Cons**

* 依存管理が分散しやすい
* 高速ではない

---

### Poetry

**Pros**

* 高機能
* 実績が豊富

**Cons**

* uv と比較すると依存解決・インストール速度で劣る
* 本プロジェクトで必要な機能を超えている

---

### PDM

**Pros**

* PEP 582 対応
* pyproject.toml ベース

**Cons**

* 採用実績が比較的少ない
* チームの知見が少ない

---

### uv（採用）

**Pros**

* 非常に高速
* pyproject.toml を標準利用
* 仮想環境・依存管理を一元化できる
* モノレポとの相性が良い

**Cons**

* 比較的新しいツールである
* チームメンバーに学習が必要

---

## Consequences

### Positive

* 全サービスで同じ開発環境を利用できる
* 開発手順が統一される
* CI/CD を簡素化できる
* AI エージェントへの実装指示を標準化できる

### Negative

* 全開発者が同じツールチェーンを利用する必要がある
* ツール更新時はプロジェクト全体への影響を考慮する必要がある

---

## Implementation Guidelines

すべての Python サービスは以下に従う。

* `pyproject.toml` を使用する
* 依存関係は `uv` で管理する
* コードフォーマットは Ruff Format を使用する
* 静的解析は Ruff と basedpyright を使用する
* テストは Pytest を使用する
* Git Hooks は pre-commit を利用する

具体的な実行手順は以下のとおりである。

```bash
uv sync --group dev
uv run pre-commit install
uv run ruff check .
uv run ruff format --check .
uv run basedpyright
uv run pytest
```

サービス固有の設定は、プロジェクト標準を変更しない範囲で追加できる。

---

## Future Considerations

今後ツールチェーンを変更する場合は、本ADRを更新し、影響範囲を評価した上で移行計画を策定する。
