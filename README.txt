Project Physical AI Partner

このリポジトリでは、ローカル実行を前提とした AI アバター基盤の設計方針を管理します。

主なドキュメント:
- docs/architecture/microservices-architecture.md
- docs/adr/0001-microservices-architecture.md

方針の要点:
- GPU 制約のある環境でも独立したサービスとして構築する
- NATS ベースのイベント駆動通信を採用する
- サービス間でデータベースを直接共有しない
