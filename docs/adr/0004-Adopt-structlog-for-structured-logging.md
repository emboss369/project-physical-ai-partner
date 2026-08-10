# 0004: Adopt Structlog for Structured Logging

**Status:** Accepted

**Date:** 2026-08-11

## Context

Project Physical AI Partner はマイクロサービスアーキテクチャを採用する。

各サービス（Gateway、Audio、ASR、LLM、Agent、Memory、TTS、Avatar）は独立したプロセスとして動作し、ログは障害解析、デバッグ、監視、および将来の Observability 基盤で利用される。

サービスごとに独自のログ設定を実装すると、ログフォーマットや出力方法が統一されず、分析や保守が困難になる。

そのため、プロジェクト全体で共通のロギングライブラリを採用する。

---

## Decision

プロジェクト標準のロギングライブラリとして **structlog** を採用する。

すべてのサービスは `shared.logging` を通じて Logger を取得する。

サービスコードから Python 標準の `logging` を直接設定してはならない。

---

## Alternatives Considered

### Python Standard Library (`logging`)

**Pros**

* 標準ライブラリ
* 追加依存なし
* 実績が豊富

**Cons**

* 構造化ログが扱いにくい
* Context情報の付与が煩雑
* JSONログの設定が複雑

---

### Loguru

**Pros**

* API がシンプル
* 学習コストが低い

**Cons**

* 標準 logging との統合が必要
* ライブラリ開発より小規模アプリ向き

---

### Structlog（採用）

**Pros**

* Structured Logging を前提としている
* JSON 出力との親和性が高い
* Context 情報を扱いやすい
* OpenTelemetry との統合が容易
* Python 標準 logging と共存できる

**Cons**

* 追加ライブラリが必要
* 初期設定がやや複雑

---

## Consequences

### Positive

* 全サービスでログフォーマットを統一できる
* JSONログを標準化できる
* Correlation ID を容易に付与できる
* Loki や Grafana などのログ基盤と統合しやすい
* 将来的な OpenTelemetry 導入が容易になる

### Negative

* 新しいライブラリへの依存が追加される
* 開発者が structlog の利用方法を理解する必要がある

---

## Implementation Guidelines

ロガーは `shared.logging` を通じて取得する。

例：

```python
from shared.logging import get_logger

logger = get_logger(__name__)

logger.info(
    "LLM request",
    model="qwen3",
    session_id=session_id,
)
```

サービスは logging の設定を持たず、共通ライブラリが設定を管理する。

---

## Future Considerations

将来的に以下を段階的に追加する。

* Correlation ID
* Trace ID
* OpenTelemetry
* Loki
* Grafana
* Prometheus
* Audit Log

これらは `shared.logging` の内部実装として追加し、サービス側のコード変更を不要とする。
