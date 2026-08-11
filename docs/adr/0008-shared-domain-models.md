# ADR-0008: Shared Domain Models

- Status: Accepted
- Date: 2026-08-11

## Context

複数サービスが Session、Conversation、Transcript、LLMMessage など同じ概念を扱う。各サービスがこれらを個別に定義すると、型、検証、意味が徐々に不一致になる。一方、サービス固有の内部表現まで共有すると、サービス境界が失われる。

## Decision

複数サービスで同じ意味とライフサイクルを持つ安定概念だけを Shared Domain Model とし、`shared/src/shared/models/` にPydanticモデルとして配置する。

モデルは原則として `frozen=True` の不変モデルとする。作成時に型・値・関係を検証し、変更は新しいモデルを生成して表現する。継承は避け、モデルの合成を優先する。

### Shared model candidates

- `Session`
- `Conversation`
- `Transcript`
- `AudioChunk`
- `LLMMessage`
- `ToolCall`
- `ToolResult`

候補は、少なくとも2つのサービスが同じ意味で利用し、特定サービスの実装詳細を含まない場合だけ共有モデルに昇格できる。

### Responsibilities and boundaries

| Type | Responsibility | Location |
| --- | --- | --- |
| Shared Domain Model | サービス横断で安定した業務概念 | `shared/models/` |
| Event Contract | サービス間の配送用エンベロープとpayload | `shared/contracts/` |
| API DTO | 外部またはサービスAPIの入出力 | API境界の近く |
| Database Entity / ORM Model | 永続化のための表現 | 各サービスのinfrastructure層 |
| Internal Model | サービス固有の処理詳細 | 各サービス内部 |

Shared Domain ModelをEvent ContractやORMモデルとして直接送受信・永続化してはならない。必要な変換は各境界で明示する。

### Versioning and compatibility

- 任意フィールドの追加と、既存の意味を変えない制約緩和のみを後方互換とする。
- フィールド削除、名前・型・意味の変更、必須フィールド追加は破壊的変更とする。
- 破壊的変更は新しいモデル名またはメジャーバージョンを導入し、移行期間中は旧モデルを維持する。
- 共有モデルの変更は利用サービスへの影響をレビューする。

## Alternatives Considered

### Service-local models only

サービスの独立性は高いが、同じ概念の重複定義と意味のずれを防げないため採用しない。

### Shared ORM models

永続化実装とドメイン概念が密結合になり、データベースプロバイダを交換可能にする方針に反するため採用しない。

### Mutable data classes

変更追跡が難しく、非同期イベント処理で意図しない共有状態を作りやすいため採用しない。

## Consequences

### Positive

- サービス横断の概念と検証規則を統一できる。
- 不変性によりイベント処理と並行処理での意図しない変更を減らせる。
- API、イベント、永続化の境界を明確に維持できる。

### Negative

- 共有モデルへ昇格するかの判断と影響レビューが必要になる。
- 変換コードが増えるが、境界ごとの責務が明確になる。
