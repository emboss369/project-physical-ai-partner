# API 契約とイベント仕様

## 1. 共通原則

- すべてのサービスは JSON 形式でやり取りする
- すべてのイベントには `event_id`, `timestamp`, `source_service`, `target_service` を含める
- 失敗時は `error` オブジェクトを返す
- すべての ID は UUID 形式を基本とする

## 2. 共通スキーマ

### BaseEvent

```json
{
  "event_id": "uuid",
  "timestamp": "2026-08-11T12:00:00Z",
  "source_service": "audio-service",
  "target_service": "asr-service",
  "version": 1
}
```

### ErrorResponse

```json
{
  "error": {
    "code": "SERVICE_UNAVAILABLE",
    "message": "The requested service is unavailable"
  }
}
```

## 3. REST API 契約

### gateway-service

#### POST /voice/session

```json
{
  "session_id": "uuid",
  "user_id": "uuid",
  "device_id": "mic-01"
}
```

レスポンス:

```json
{
  "session_id": "uuid",
  "status": "active"
}
```

### memory-service

#### POST /memory/save

```json
{
  "session_id": "uuid",
  "user_id": "uuid",
  "text": "会話本文"
}
```

レスポンス:

```json
{
  "memory_id": "uuid",
  "status": "saved"
}
```

#### POST /memory/search

```json
{
  "session_id": "uuid",
  "user_id": "uuid",
  "query": "最近の予定について"
}
```

レスポンス:

```json
{
  "results": [
    {
      "memory_id": "uuid",
      "text": "関連する会話本文",
      "score": 0.91
    }
  ]
}
```

## 4. イベント名

### 音声・認識系

- `audio.detected`
- `audio.segmented`
- `asr.request`
- `asr.completed`
- `asr.failed`

### 対話・生成系

- `llm.request`
- `llm.completed`
- `llm.failed`
- `agent.request`
- `agent.completed`

### TTS・アバター系

- `tts.request`
- `tts.completed`
- `tts.failed`
- `avatar.speak`
- `avatar.expression.updated`

### Memory 系

- `memory.save.request`
- `memory.save.completed`
- `memory.search.request`
- `memory.search.completed`
- `memory.search.failed`

## 5. イベントスキーマ

### audio.detected

```json
{
  "event_id": "uuid",
  "timestamp": "2026-08-11T12:00:00Z",
  "source_service": "audio-service",
  "target_service": "asr-service",
  "version": 1,
  "payload": {
    "session_id": "uuid",
    "audio_chunk_id": "uuid",
    "sample_rate": 16000,
    "format": "pcm16"
  }
}
```

### asr.completed

```json
{
  "event_id": "uuid",
  "timestamp": "2026-08-11T12:00:00Z",
  "source_service": "asr-service",
  "target_service": "llm-service",
  "version": 1,
  "payload": {
    "session_id": "uuid",
    "transcript": "今日の予定を教えて",
    "language": "ja"
  }
}
```

### llm.completed

```json
{
  "event_id": "uuid",
  "timestamp": "2026-08-11T12:00:00Z",
  "source_service": "llm-service",
  "target_service": "tts-service",
  "version": 1,
  "payload": {
    "session_id": "uuid",
    "response_text": "明日の会議は 10 時です",
    "finish_reason": "stop"
  }
}
```

### memory.save.request

```json
{
  "event_id": "uuid",
  "timestamp": "2026-08-11T12:00:00Z",
  "source_service": "agent-service",
  "target_service": "memory-service",
  "version": 1,
  "payload": {
    "session_id": "uuid",
    "user_id": "uuid",
    "text": "会話本文"
  }
}
```

### memory.search.request

```json
{
  "event_id": "uuid",
  "timestamp": "2026-08-11T12:00:00Z",
  "source_service": "agent-service",
  "target_service": "memory-service",
  "version": 1,
  "payload": {
    "session_id": "uuid",
    "user_id": "uuid",
    "query": "最近の予定について"
  }
}
```

### memory.search.completed

```json
{
  "event_id": "uuid",
  "timestamp": "2026-08-11T12:00:00Z",
  "source_service": "memory-service",
  "target_service": "agent-service",
  "version": 1,
  "payload": {
    "session_id": "uuid",
    "results": [
      {
        "memory_id": "uuid",
        "text": "関連する会話本文",
        "score": 0.91
      }
    ]
  }
}
```
