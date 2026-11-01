# CampusMIND 2.0 Architectural & Reference Documentation Index

This index links the primary architectural specifications and technical foundations used in the synthesis of the CampusMIND 2.0 Comprehensive Technical Report.

1. **System Architecture Document** (`docs/architecture.md`)
   - Decoupled modular monolith structure, repository patterns, correlation middleware, and service interfaces.
2. **Advanced RAG Architecture Specification** (`docs/RAG_ARCHITECTURE.md`)
   - Document chunking, hybrid BM25 + cosine scoring, deterministic hybrid reranker, and evidence quality signals.
3. **Database & Identity Architecture** (`docs/DATABASE_ARCHITECTURE.md`)
   - Relational schema normalization, SQLAlchemy 2.x ORM models, connection pooling parameters, and Alembic migrations.
4. **Academic Analytics & Intelligence Architecture** (`docs/ANALYTICS_ARCHITECTURE.md`)
   - Attendance deficit formulas, consecutive recovery calculus $N = \lceil (0.75 \cdot C - A) / 0.25 \rceil$, and performance guidance.
5. **Phase 8 Production & Scalability Architecture** (`docs/PHASE8_PRODUCTION_ARCHITECTURE.md`)
   - BackgroundTaskManager state machines, real-time SSE notification stream transport, and secret-masking filters.
6. **Object Knowledge Foundation (OKF) Graph Engine** (`backend/okf/`)
   - Graph ontology definitions, Pydantic triple validation, recursive CTE neighbor queries, and hybrid knowledge agents.
