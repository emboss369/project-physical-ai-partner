# AGENTS.md

Version: 1.0.0
Last Updated: 2026-08-11

# Project Physical AI Partner

This document defines the engineering principles for all AI agents
(Codex, ChatGPT, Claude Code, Gemini CLI, and future AI development tools)
working on this repository.

This document is the development constitution of Project Physical AI Partner.

---

# Project Vision

Project Physical AI Partner is a fully local AI partner designed for
long-term software engineering, robotics, and research projects.

The goal is NOT to build a chatbot.

The goal is to build an AI project partner that grows together with the user.

The architecture should remain maintainable for many years and continue to
support future AI technologies with minimal redesign.

---

# Design Philosophy

Beautiful Architecture First.

When multiple solutions are possible, prefer the one that:

- is easier to understand
- has clearer interfaces
- reduces coupling
- improves maintainability
- improves testability
- is easier to extend
- minimizes technical debt

Do not optimize for the current implementation.

Optimize for the next ten years.

---

# Communication

All communication with the repository owner should be conducted in Japanese.

The following may remain in English:

- Source code
- API names
- Class names
- Function names
- Variable names
- Technical terminology
- Protocol names

Documentation may be written in either Japanese or English depending on the target audience.

When uncertain, communicate in Japanese.

---

# AI Collaboration

This repository is developed collaboratively by humans and AI agents.

AI agents should:

- Ask questions whenever requirements are ambiguous.
- Suggest improvements when appropriate.
- Point out architectural concerns.
- Explain important design trade-offs.
- Never silently assume missing requirements.

Asking questions is always preferred over implementing the wrong solution.

---

# Architectural Decisions

Major architectural decisions must never be made unilaterally by AI agents.

Examples include:

- Framework changes
- Database changes
- Directory restructuring
- Service decomposition
- Communication protocols
- Dependency replacement

When uncertain:

Stop.

Explain the issue.

Ask for approval.

Never surprise the user.

---

# Core Principles

## Local First

Everything should work locally whenever possible.

Cloud services are optional.

Preferred technologies include:

- Parakeet ASR
- Qwen3
- Qwen3-TTS
- SQLite
- FAISS
- vLLM
- SGLang

Cloud providers should always be optional providers.

---

## Modular Design

Every major subsystem must be replaceable.

Avoid tight coupling.

Every implementation should depend on interfaces rather than concrete implementations.

---

## Service Oriented

Design each subsystem as an independent service.

Examples:

- Memory Service
- LLM Service
- Agent Service
- Persona Service
- Avatar Service
- ASR Service
- TTS Service
- Dashboard Service
- MCP Service

---

## Provider Pattern

External systems must be implemented as interchangeable providers.

Never call vendor-specific APIs directly outside provider implementations.

---

## Persona is Data

Personas must never be hardcoded.

Store personas as data.

Example:

```
personas/
    midori/
        persona.yaml
        avatar.vrm
        memories.db
```

Future personas should be addable without code changes.

---

## Event Driven

Prefer event-driven communication over direct service coupling.

Example:

```
ASR Finished
        ↓
   Event Bus
        ↓
Memory Service
        ↓
Agent Service
        ↓
Avatar Service
        ↓
Logging
```

---

## Human in Control

AI agents must never perform dangerous operations without explicit approval.

Examples:

- git push
- git tag
- release creation
- deleting files
- deleting databases
- terraform destroy
- production configuration changes

Always ask first.

---

# Architecture

Prefer Clean Architecture.

```
UI
    ↓
Application
    ↓
Domain
    ↓
Infrastructure
```

Dependencies must always point inward.

Business logic must never depend on infrastructure.

---

# Coding Style

Target:

- Python 3.12+

Quality tools:

- Ruff
- Pyright
- Pytest

Formatting:

```
ruff format
```

Lint:

```
ruff check
```

Typing:

Use static typing whenever practical.

Avoid unnecessary complexity.

Readable code is preferred over clever code.

---

# Documentation

Public APIs should include docstrings.

Complex algorithms should include design comments.

Keep README and documentation synchronized with implementation.

Architecture changes must update architecture documentation.

---

# Testing

Every feature should include appropriate tests.

Prefer:

- Unit tests
- Integration tests where appropriate

New features should not reduce test coverage.

---

# Performance

Measure before optimizing.

Avoid premature optimization.

The Memory Service should scale to millions of memories.

Performance optimizations must not sacrifice maintainability.

---

# Database

Current primary database:

- SQLite

Current vector database:

- FAISS

Future providers may include:

- PostgreSQL + pgvector
- Qdrant
- Milvus

Database implementations must remain replaceable.

---

# Dependency Policy

Prefer the Python standard library whenever practical.

Avoid unnecessary dependencies.

Every additional dependency should have a clear justification.

---

# Error Handling

Never silently ignore exceptions.

Provide meaningful error messages.

Log enough information for troubleshooting.

Avoid exposing sensitive information.

---

# Security

Never commit secrets.

Use environment variables or `.env`.

Validate all external input.

Avoid unnecessary privileges.

---

# Git Workflow

Prefer:

- Small commits
- Clear commit messages
- One logical change per commit

Do not mix:

- Refactoring
- Feature implementation
- Formatting-only changes

into a single commit.

---

# Development Philosophy

Code is written for humans.

AI generates code.

Humans maintain code.

Maintainability is more important than cleverness.

Simplicity is more important than unnecessary abstraction.

---

# Priority Order

When trade-offs exist, prioritize in the following order:

1. Correctness
2. Maintainability
3. Extensibility
4. Readability
5. Performance
6. Convenience

---

# Definition of Done

A task is complete only when:

- Implementation is complete
- Tests pass
- Ruff passes
- Pyright passes
- Documentation is updated
- Examples are updated when applicable

---

# Long-term Goal

Build an AI partner capable of supporting years of:

- Software engineering
- Robotics
- Research
- Knowledge management
- Project management

The system should remain maintainable even after growing to hundreds of thousands of lines of code.

Always prioritize long-term architecture over short-term convenience.