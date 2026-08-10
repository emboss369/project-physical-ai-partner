# データスキーマ例

## Session

```json
{
  "session_id": "uuid",
  "user_id": "uuid",
  "created_at": "2026-08-11T12:00:00Z",
  "status": "active",
  "device_id": "mic-01"
}
```

## ConversationTurn

```json
{
  "turn_id": "uuid",
  "session_id": "uuid",
  "speaker": "user",
  "text": "こんにちは",
  "timestamp": "2026-08-11T12:00:01Z"
}
```

## MemoryRecord

```json
{
  "memory_id": "uuid",
  "session_id": "uuid",
  "user_id": "uuid",
  "text": "会話本文",
  "embedding": [0.01, 0.02, 0.03],
  "created_at": "2026-08-11T12:00:02Z"
}
```

## TTSRequest

```json
{
  "request_id": "uuid",
  "session_id": "uuid",
  "text": "こんにちは",
  "voice": "midori",
  "speed": 1.0
}
```

## AvatarAction

```json
{
  "action_id": "uuid",
  "session_id": "uuid",
  "type": "speak",
  "expression": "smile",
  "lip_sync_text": "こんにちは"
}
```
