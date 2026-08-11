# Shared Library

`shared` は、複数サービスから利用する安定した契約と再利用可能なライブラリのための Python パッケージです。

## Development

リポジトリルートで依存関係を同期します。

```bash
uv sync
```

ワークスペースのパッケージは開発用仮想環境にインストールされるため、サービスやテストから次のように import できます。

```python
from shared.sample import get_package_name
```

## Layout

```text
shared/
├── src/shared/  # Python package
├── tests/       # Shared library tests
├── pyproject.toml
└── README.md
```

## Rules

- 複数サービスで同じ意味を持つ契約・機能だけをここに置く。
- サービス固有の業務ロジックは `services/` に置く。
- `shared` は特定サービスに依存してはならない。
- 新しい公開モジュールにはテストを追加し、利用方法を文書化する。
