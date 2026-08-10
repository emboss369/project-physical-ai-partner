# マイクロサービスアーキテクチャ

## 目的

Project Physical AI Partner は、ローカル実行を前提にした AI アバター基盤として設計する。\nGPU メモリ制約がある環境でも、各機能を独立して起動・停止・再配置できるようにし、将来のスケールと保守性を確保する。

## 基本方針

- 1 つの巨大プロセスで全機能を実装しない
- GPU を必要なサービスだけに割り当てる
- サービス間は API またはイベント経由でのみ連携する
- 共有データベースは避け、各サービスが自身のデータを保持する
- 将来、LLM / TTS / Avatar を別マシンへ移設しやすい構造にする

## 全体構成

```text
User
  |
  v
gateway-service
  |
  v
NATS / Redis Streams
  |
  +--> audio-service
  +--> asr-service
  +--> llm-service
  +--> agent-service
  +--> tts-service
  +--> avatar-service
  +--> memory-service
  +--> tool-service
  +--> monitor-service
```

## サービス一覧

- gateway-service
  - WebSocket / REST の入口
  - 認証、ルーティング、接続管理

- audio-service
  - マイク入力
  - VAD
  - 録音
  - ノイズ除去

- asr-service
  - SenseVoice などの音声認識
  - ストリーミング認識

- llm-service
  - Qwen3 を利用した対話生成
  - vLLM / SGLang などの推論基盤
  - GPU 専有

- agent-service
  - 会話制御
  - MCP 連携
  - Tool Calling
  - Memory / RAG 連携

- tts-service
  - Qwen3-TTS
  - 音声設定・話者制御

- avatar-service
  - VRM 表示
  - BlendShape / LipSync / Expression / Motion

- memory-service
  - 会話履歴
  - 埋め込み
  - SQLite / Qdrant などの保存基盤
  - Save() で本文を SQLite に保存し、同時に埋め込みを生成して FAISS に登録する
  - Search(query) でクエリ埋め込みを作成し、FAISS から Top-K ID を取得した後、SQLite から本文を復元する

- tool-service
  - ブラウザ操作
  - 検索
  - 天気情報
  - Google 連携

- monitor-service
  - Health Check
  - Prometheus / Grafana 連携
  - ログ・メトリクス収集

## GPU 配分の方針

RTX 5060 Ti 16GB を想定し、以下のように負荷を分散する。

- GPU
  - LLM
  - ASR
- CPU
  - Agent
  - MCP
  - Memory
  - Avatar
- TTS
  - 必要時のみ GPU を利用し、発話終了後に GPU を解放する

将来 GPU を増設した場合は、次のように分離しやすい。

- GPU0: LLM
- GPU1: TTS

## 通信方式

REST ではなく NATS を主系統として採用する。

### memory-service の内部データフロー

```text
Save()
  |
  v
SQLite
  (会話本文)
  |
  +--> Embedding
        |
        v
      FAISS
      (ベクトル索引)

Search(query)
  |
  v
Top-K IDs
  |
  v
SQLite から本文取得
```

典型的なイベント例:

```text
mic -> audio.detected
audio.detected -> asr.request
asr.completed -> llm.request
llm.completed -> tts.request
tts.completed -> avatar.speak
```

この方式により、各サービスはイベントを送受信するだけでよく、結合度を下げられる。

## モノレポ構成

```text
project-physical-ai-partner/
├── services/
│   ├── gateway-service/
│   ├── audio-service/
│   ├── asr-service/
│   ├── llm-service/
│   ├── agent-service/
│   ├── tts-service/
│   ├── avatar-service/
│   ├── memory-service/
│   ├── tool-service/
│   └── monitor-service/
├── shared/
│   ├── contracts/
│   ├── proto/
│   ├── models/
│   ├── config/
│   ├── logging/
│   └── utils/
├── infra/
│   ├── docker/
│   ├── compose/
│   └── k8s/
├── docs/
│   ├── architecture/
│   ├── adr/
│   └── api/
├── tests/
│   ├── integration/
│   ├── e2e/
│   └── performance/
└── README.md
```

## 設計原則

1. サービス間で直接データベースを共有しない
2. API またはイベント経由でのみ連携する
3. 各サービスは独立して再起動できること
4. GPU リソースは必要なサービスへ局所的に割り当てる
5. 将来の機械追加・再配置を前提にして境界を明確にする

## 契約とスキーマの管理先

- API 契約: docs/api/contracts.md
- スキーマ例: docs/api/schema-examples.md
