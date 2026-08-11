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

## Logging

すべてのサービスは標準ライブラリの `logging` を直接設定せず、`shared.logging` を利用します。

```python
from shared.logging import configure_logging, get_logger

configure_logging(level="INFO", json_logs=False)
logger = get_logger(__name__)
logger.info("application_started", service="agent-service")
```

本番向けのJSON出力は `configure_logging(json_logs=True)` を指定します。サービス間の追跡に必要な値は、contextvarsを使ってバインドします。

```python
from shared.logging import bind_context

bind_context(correlation_id="request-123")
```

機密情報、音声データ、会話全文をログへ出力してはなりません。詳細は ADR-0005 を参照してください。

## Configuration

サービス固有の設定は `BaseServiceSettings` を継承して定義します。サービスコードで `os.environ` を直接参照してはなりません。

```python
from shared.config import BaseServiceSettings, service_settings_config


class LlmSettings(BaseServiceSettings):
    model_config = service_settings_config(env_prefix="LLM_")

    model_name: str
    max_tokens: int = 512
```

環境変数にはサービス固有の接頭辞を付け、ネストした値は `__` で表現します。例: `LLM_MODEL__MAX_TOKENS=1024`。`.env` はローカル開発用であり、Git管理してはなりません。
