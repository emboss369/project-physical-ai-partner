# ADR-0007: Adopt Event Contract Architecture

- Status: Accepted
- Date: 2026-08-11

## Context

Project Physical AI Partner のサービスはNATSを主系統とするイベント駆動通信で連携する。サービス固有のデータ構造を直接送受信すると、通信相手への依存、互換性のない変更、障害追跡の困難さが生じる。

サービス境界で交換するメッセージを明示的な契約として定義し、型検証、追跡、段階的な進化を可能にする必要がある。

## Decision

イベント契約は **Pydanticモデルで定義し、UTF-8 JSONでシリアライズする**。各メッセージは共通エンベロープとイベント固有のpayloadで構成する。

Pydanticモデルは `shared/contracts/` に置き、送信前と受信時に検証する。JSON Schemaは必要に応じてPydanticモデルから生成し、外部連携やドキュメントに利用する。初期段階ではProtocol Buffers、Avro、MessagePackを採用しない。

### Message model

- **Command**: 特定サービスに処理を依頼する命令。命令形を使用する。
- **Event**: 発生済みの事実を通知するメッセージ。完了形または状態を使用する。
- **Request**: NATS request-replyで処理を問い合わせるメッセージ。
- **Response**: Requestへの応答。非同期の状態通知には使用しない。

### Envelope

すべてのメッセージは次のメタデータを持つ。

| Field | Purpose |
| --- | --- |
| `message_id` | メッセージを一意に識別するUUID |
| `correlation_id` | 一連のユーザー要求を追跡するUUID |
| `causation_id` | 生成元となったメッセージのID。起点では省略可 |
| `timestamp` | UTCのRFC 3339タイムスタンプ |
| `source_service` | 送信サービス名 |
| `message_type` | `command`、`event`、`request`、`response` のいずれか |
| `schema_version` | 契約のメジャー・マイナーバージョン |
| `payload` | メッセージ固有の検証済みデータ |

### Naming and versioning

- NATS subjectとイベント名はドット区切り・英小文字を使用する。例: `speech.recognized`、`llm.response.generated`、`tts.completed`。
- Commandは命令形を使用する。例: `asr.transcribe`。
- イベントは過去形または完了状態を使用する。例: `audio.detected`、`transcription.completed`。
- 既存フィールドの削除、名前変更、型変更、意味変更は破壊的変更とする。
- 任意フィールドの追加と既存フィールドの意味を変えない拡張だけを後方互換とする。
- 破壊的変更では新しいメジャーバージョンの契約とsubjectを作成し、旧契約は移行期間中維持する。
- Consumerは未知の任意フィールドを無視できなければならない。

### Delivery rules

- Consumerは `message_id` を使って冪等に処理する。
- `correlation_id` はログコンテキストへ引き継ぎ、サービス横断の追跡に使用する。
- payloadに秘密情報、音声データ本体、会話全文を含めない。大きなデータは参照先を別途契約で表現する。

## Alternatives Considered

### Protocol Buffers

言語横断のコード生成、コンパクトなバイナリ形式、強い進化規則を提供する。一方で、`.proto`の管理とコード生成の導入コストがあり、現時点のPython中心・ローカル中心のサービス構成には過剰である。多言語サービスや帯域最適化が必要になった時点で再評価する。

### JSON Schema

標準化されたJSONの検証仕様として外部連携に適している。しかしPythonの実行時モデル、型検証、シリアライズを別々に実装する必要があるため、内部契約の主定義には採用しない。Pydanticから生成する派生成果物として利用する。

### Apache Avro

スキーマ進化とストリーミングデータに適するが、初期段階のNATSメッセージングにはスキーマレジストリを含む運用負荷が大きい。

## Consequences

### Positive

- Pythonサービス間の契約を型安全かつ可読な形で共有できる。
- JSONによりNATSメッセージのデバッグと運用観測が容易になる。
- 相関IDと因果IDにより分散処理を追跡できる。
- 互換性規則によりサービスを段階的に更新できる。

### Negative

- JSONはProtocol Buffersよりサイズ・速度で劣る。
- 契約変更時に互換性レビューとConsumer影響確認が必要になる。
- Pydanticモデルと生成JSON Schemaの同期を維持する必要がある。
