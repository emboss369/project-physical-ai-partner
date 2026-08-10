# ADR 0002: Repository Structure

- Status: Accepted
- Date: 2026-08-11

## Context

Project Physical AI Partner は、複数の独立したサービスと、それらで共有する契約・ライブラリを単一のリポジトリで開発する。サービス数の増加後も、コードの配置場所と依存方向を一貫させ、変更範囲を把握しやすくする必要がある。

## Decision

リポジトリは次のトップレベルディレクトリを持つモノレポとする。

```text
project-physical-ai-partner/
├── services/   # 独立して実行・デプロイ可能なサービス
├── shared/     # 複数サービスで共有する契約とライブラリ
├── docs/       # 永続的なプロジェクト文書
├── scripts/    # 開発・運用・CIを補助するスクリプト
├── tests/      # サービス横断のテスト
├── AGENTS.md
└── README.md
```

### Naming rules

- ディレクトリ名とMarkdownファイル名は、英小文字の kebab-case を使用する。
- サービスディレクトリは `<capability>-service` とする。例: `llm-service`、`memory-service`。
- Python パッケージ名とモジュール名は snake_case を使用する。
- ADR は `docs/adr/NNNN-<decision>.md` とし、`NNNN` は4桁の連番とする。
- 略語は既存の技術名称である `api`、`llm`、`tts`、`asr`、`vrm` を除き、読みやすい単語で記述する。

### `services/`

各サービスは独立した所有単位であり、サービス固有のアプリケーションコード、設定、ユニットテストをその配下に置く。サービス間の共有を目的としたコードは置かない。

将来のサービスは次の構造を基準とする。

```text
services/
└── <capability>-service/
    ├── src/       # サービスのアプリケーションコード
    ├── tests/     # サービス固有のユニットテスト
    ├── README.md  # 責務、起動方法、依存契約
    └── pyproject.toml
```

### `shared/`

`shared/` には、複数サービスが同じ意味で利用するものだけを配置する。ドメイン固有の業務ロジックは各サービスに残し、循環依存を作らない。

- `contracts/`: イベント、API、データスキーマなどのサービス間契約
- `config/`: 共通設定の読み込み・検証基盤
- `observability/`: 共通ログ、メトリクス、トレーシングの基盤
- `testing/`: 複数サービスで再利用するテストフィクスチャとテスト支援コード

共有ライブラリを追加するときは、利用サービスと依存方向を明確にし、特定サービスへの依存を持たせない。

### `docs/`

- `adr/`: 採用済みの設計判断とその背景
- `architecture/`: システム全体・サービス境界・データフロー
- `api/`: 外部およびサービス間の契約
- `design/`: 詳細設計、UI/UX、コンポーネント設計

### `scripts/` and `tests/`

`scripts/` には開発、運用、CIを支援する再利用可能なスクリプトのみを置き、サービスの実行コードは置かない。`tests/` には、複数サービスをまたぐ integration、end-to-end、performance テストを置く。ユニットテストは対象サービスの `tests/` に置く。

## Consequences

### Positive

- サービスの責務と所有範囲を明確にできる。
- 共有契約を明示的に管理でき、サービス間通信の変更を追跡しやすい。
- テストの粒度と実行範囲を整理できる。
- サービス追加時に配置判断を繰り返さずに済む。

### Negative

- 小さな変更でも共有コードの配置可否を検討する必要がある。
- 共有ライブラリの変更は複数サービスへの影響確認が必要になる。
