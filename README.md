# Project Physical AI Partner

ローカル環境で動作する、長期的なソフトウェア開発・ロボティクス・研究を支援する AI パートナーの基盤です。

## Repository structure

```text
project-physical-ai-partner/
├── docs/       # ADR, architecture, API, and detailed design documentation
├── scripts/    # Development, operational, and CI support scripts
├── services/   # Independently deployable application services
├── shared/     # Cross-service contracts and reusable libraries
├── tests/      # Cross-service integration, end-to-end, and performance tests
├── AGENTS.md   # Engineering principles for AI agents
└── README.md
```

各サービスは独立して実装・再起動できることを目指し、サービス間の連携にはイベント駆動の通信を採用します。詳細は [マイクロサービスアーキテクチャ](docs/architecture/microservices-architecture.md) と [ADR-0001](docs/adr/0001-microservices-architecture.md) を参照してください。

配置ルール、命名規則、サービスおよび共有コードの構成は [ADR-0002: Repository Structure](docs/adr/0002-repository-structure.md) に従います。

## Documentation

- [Architecture](docs/architecture/)
- [Architecture Decision Records](docs/adr/)
- [API contracts](docs/api/)
- [Detailed design](docs/design/)
- [AI development workflow](docs/ai-development-workflow.md)
