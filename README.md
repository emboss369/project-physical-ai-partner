# Project Physical AI Partner

ローカル環境で動作する、長期的なソフトウェア開発・ロボティクス・研究を支援する AI パートナーの基盤です。

## Repository structure

```text
project-physical-ai-partner/
├── docs/       # Architecture, ADR, API, and design documentation
├── scripts/    # Development and operational scripts
├── services/   # Independently deployable application services
├── shared/     # Reusable libraries and cross-service contracts
├── AGENTS.md   # Engineering principles for AI agents
└── README.md
```

各サービスは独立して実装・再起動できることを目指し、サービス間の連携にはイベント駆動の通信を採用します。詳細は [マイクロサービスアーキテクチャ](docs/architecture/microservices-architecture.md) と [ADR-0001](docs/adr/0001-microservices-architecture.md) を参照してください。

## Documentation

- [Architecture](docs/architecture/)
- [Architecture Decision Records](docs/adr/)
- [API contracts](docs/api/)
- [AI development workflow](docs/ai-development-workflow.md)
