# ADR-0009: Continuous Integration Policy

- Status: Accepted
- Date: 2026-08-11

## Context

Project Physical AI Partner はモノレポ上で複数のマイクロサービスを開発する。人間とAIエージェントが同じ品質基準で変更を検証し、`main` ブランチの品質を維持するために、短時間で失敗を検知できるCIが必要である。

## Decision

GitHub ActionsをContinuous Integration（CI）に採用する。すべてのPull RequestはCIを通過しなければ `main` にマージしてはならない。

通常のCIは短時間で完了するチェックに限定し、長時間実行されるテスト・ベンチマークは別ワークフローで管理する。

### Triggers

- Pull Requestの作成・更新
- `main` ブランチへのPush

Releaseブランチやタグ用のワークフローは必要になった時点で追加する。

### Required checks

CIは次の順で実行する。

1. Python 3.12環境のセットアップ
2. `uv sync` による依存関係の同期
3. `ruff format --check .`
4. `ruff check .`
5. `basedpyright`
6. `pytest`

すべてが成功した場合だけCIを成功とする。ローカル開発でも同じコマンドを実行できなければならない。

### Branch protection

`main` には次の保護ルールを設定する。

- Pull Requestを経由した変更だけを許可する。
- 必須CIチェックの成功後だけマージを許可する。
- レビューを最低1件要求する。必要に応じてプロジェクト管理者が変更できる。

### Performance policy

- 通常のCIは3分以内、最長5分以内を目標とする。
- uvの依存関係キャッシュを利用する。
- E2Eテスト、GPU推論テスト、音声モデルのダウンロード、LLM実推論、ベンチマーク、負荷試験は通常CIに含めない。

### AI-assisted development

AIエージェントが生成した変更にも、人間の変更と同じCI基準を適用する。CIを通過しない変更は品質基準を満たしていないものとして扱う。

## Consequences

### Positive

- `main` の品質を継続的に維持できる。
- 不具合と規約違反を早期に検出できる。
- 人間とAIエージェントに同一の検証基準を適用できる。

### Negative

- GitHub Actionsワークフローとキャッシュの保守が必要になる。
- 一時的なCI障害によりマージが遅延する可能性がある。

## Future Considerations

Integration Test、E2E Test、Security Scan、依存関係脆弱性スキャン、ライセンス検査、ドキュメントビルド、リリース自動化は、通常CIと分離したワークフローとして追加を検討する。
