# ADR-0005: Logging Policy

**Status:** Accepted

**Date:** 2026-08-11

## Context

Project Physical AI Partner はマイクロサービスアーキテクチャを採用する。

ログは単なるデバッグ出力ではなく、システム運用・障害解析・監査・Observability を支える重要な情報源である。

各サービスが独自のルールでログを出力すると、分析・検索・トレースが困難になるため、プロジェクト全体で統一したログポリシーを定める。

---

## Decision

すべてのサービスは本ポリシーに従ってログを出力する。

ログは構造化（Structured Logging）を前提とし、JSON形式で出力できることを基本とする。

---

# Logging Levels

以下のログレベルを使用する。

| Level    | Purpose         |
| -------- | --------------- |
| DEBUG    | 詳細なデバッグ情報       |
| INFO     | 通常の処理・状態遷移      |
| WARNING  | 異常ではないが注意が必要な事象 |
| ERROR    | 処理継続が困難なエラー     |
| CRITICAL | システム全体に影響する重大障害 |

---

# Required Fields

すべてのログには可能な限り以下の情報を含める。

| Field     | Description   |
| --------- | ------------- |
| timestamp | UTC Timestamp |
| level     | Log Level     |
| service   | サービス名         |
| logger    | Logger Name   |
| event     | イベント名         |
| message   | 人が読める説明       |

---

# Correlation ID

サービス間で処理を追跡できるよう、リクエスト単位の Correlation ID を利用する。

例

```text
Gateway
    ↓
Audio
    ↓
ASR
    ↓
Agent
    ↓
LLM
    ↓
TTS
    ↓
Avatar
```

同一リクエストでは同じ Correlation ID を利用する。

---

# Structured Logging

ログは Key-Value 形式で出力する。

例

```python
logger.info(
    "Speech recognized",
    language="ja",
    duration_ms=824,
    confidence=0.96,
)
```

メッセージ文字列へ値を埋め込む形式は推奨しない。

---

# Sensitive Information

以下の情報はログへ出力してはならない。

* API Key
* Access Token
* Password
* Secret
* OAuth Token
* Cookie
* Session Secret
* 個人情報（PII）
* 音声データ本体
* 会話全文（デバッグ用途を除く）

必要に応じてマスキングまたはハッシュ化を行う。

---

# Exception Logging

例外を捕捉した場合はスタックトレースを出力する。

例外を握りつぶしてはならない。

エラーには可能な限り原因と対処可能な情報を含める。

---

# Performance Logging

以下の主要処理は処理時間を記録する。

* ASR
* LLM推論
* Tool Calling
* TTS
* Avatar制御

例

```python
logger.info(
    "LLM completed",
    latency_ms=184,
)
```

---

# Event Naming

イベント名は動詞の過去形または状態を表す名称とする。

例

* request_received
* transcription_completed
* llm_response_generated
* speech_synthesized
* avatar_animation_started

---

# Log Format

開発環境

* Console Logging

本番環境

* JSON Logging

設定により切り替え可能とする。

---

# Future Considerations

将来的に以下との統合を想定する。

* OpenTelemetry
* Trace ID
* Loki
* Grafana
* Prometheus
* Distributed Tracing

本ポリシーはこれらとの互換性を維持する。

---

## Consequences

### Positive

* 全サービスでログフォーマットが統一される
* 障害解析が容易になる
* 分散システムの追跡性が向上する
* Observability基盤へ段階的に移行できる

### Negative

* ログ出力ルールを開発者全員が遵守する必要がある
* Context情報の付与が必須となるため、実装時の意識が必要になる
