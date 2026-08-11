# ADR-0010: Adopt Coding Standards

- Status: Accepted
- Date: 2026-08-11

## Context

複数サービスを含むモノレポを、人間とAIエージェントが継続的に変更する。可読性、保守性、型安全性を一貫して維持するため、全Pythonコードに共通の規約が必要である。

## Decision

Python 3.12以降のコード品質基準として、Ruff、Ruff Format、basedpyright、Pytestを採用する。CIとローカル開発は同じチェックを実行する。

### Style and tooling

- インデントは4スペース、改行はLF、最大行長は100文字とする。
- フォーマットはRuff Format、lintとimport順序はRuffに委譲する。手作業の整形規約を追加しない。
- basedpyrightをstandardモードで実行し、エラーを許容しない。
- Pytestで新機能とバグ修正に対する適切なテストを追加する。

### Types and naming

- 公開関数・メソッドの引数と戻り値、公開属性には型ヒントを付ける。
- `Any` は外部境界など代替不能な箇所に限定し、使用理由をコードまたは型変換の近くに残す。
- Optionalな値は `T | None` で表現し、`None` を明示的に処理する。
- Package、module、function、variableは `snake_case`、classは `PascalCase`、constantは `UPPER_SNAKE_CASE` とする。
- Genericsは型安全性を高める場合だけ使用し、不要な抽象化を避ける。

### Documentation and comments

- 公開API、複雑なアルゴリズム、重要な副作用を持つコードにはGoogleスタイルdocstringを付ける。
- コメントは実装の「なぜ」を説明し、コードを逐語的に言い換えない。
- `TODO` と `FIXME` には対応するGitHub Issue番号を付ける。例: `TODO(#123): ...`。

### Error handling

- 例外を握りつぶさない。回復できない例外は、原因を保持して再送出する。
- ドメインで識別可能な失敗には独自例外を定義する。
- エラーを記録する場合は `shared.logging` を使用し、秘密情報を含めない。

### AI-assisted development

AIが生成したコードにも同じ規約を適用する。Pull Request前にRuff、Ruff Format、basedpyright、Pytestを成功させ、不要なコメント、未使用コード、未追跡の例外を残さない。

## Consequences

### Positive

- サービス間で一貫した可読性と品質を維持できる。
- 自動ツールによりレビューで扱うべき設計上の論点へ集中できる。
- AI生成コードを含め、変更の品質を客観的に検証できる。

### Negative

- 規約とツール設定の変更には全サービスへの影響確認が必要になる。
- 厳格な型検査とテストにより、初期実装の時間が増える場合がある。
