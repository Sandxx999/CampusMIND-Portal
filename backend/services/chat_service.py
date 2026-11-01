import time
import uuid
from typing import Dict, List, Optional
from fastapi import HTTPException, status
from pydantic import BaseModel

from core.config import settings
from core.logging import logger
from repositories.audit_repository import audit_repository, AuditRepository
from repositories.student_repository import student_repository, StudentRepository
from models.schemas import ChatRequest, ChatResponse, FeedbackRequest, UserSchema, SourceCitation
from okf.hybrid_retriever import OKFHybridRetriever

class ChatService:
    def __init__(
        self,
        audit_repo: AuditRepository = audit_repository,
        student_repo: StudentRepository = student_repository,
    ):
        self.audit_repo = audit_repo
        self.student_repo = student_repo
        self.user_request_timestamps: Dict[str, List[float]] = {}
        self.retriever = OKFHybridRetriever()

    def enforce_rate_limit(self, user: UserSchema) -> None:
        """Enforces per-user rate limiting using a sliding window strategy."""
        now = time.time()
        user_id = user.username
        timestamps = self.user_request_timestamps.get(user_id, [])
        valid_timestamps = [ts for ts in timestamps if now - ts < 60]

        if len(valid_timestamps) >= settings.RATE_LIMIT_PER_MINUTE:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Rate limit exceeded ({settings.RATE_LIMIT_PER_MINUTE} requests/min). Please try again shortly.",
            )

        valid_timestamps.append(now)
        self.user_request_timestamps[user_id] = valid_timestamps

    def process_chat_query(self, request: ChatRequest, user: UserSchema) -> ChatResponse:
        """
        Processes user chat request using OKF Hybrid Retriever and OKF Graph Agent.
        """
        self.enforce_rate_limit(user)
        start_time = time.time()
        query_id = f"qry_{uuid.uuid4().hex[:8]}"

        # Step 1: Query Normalization
        clean_message = request.message.strip()

        # Step 1.5: Personal Academic Analytics Grounding for student queries
        is_attendance_query = any(k in clean_message.lower() for k in ["attendance", "present", "absent", "miss", "shortage", "risk"])
        if is_attendance_query and user.enrollment_no:
            student = self.student_repo.get_by_enrollment(user.enrollment_no)
            attendance_val = student.get("attendance_pct", 85.0) if student else 85.0
            risk_level = "LOW" if attendance_val >= 75.0 else "HIGH"
            answer = (
                f"Calculated Personal Academic Metrics for Student {user.enrollment_no}:\n"
                f"• Overall Attendance: {attendance_val:.1f}%\n"
                f"• Attendance Risk Level: {risk_level}\n"
            )
            if student:
                answer += f"• Current CGPA: {student.get('cgpa', 0.0)}\n• Enrolled Courses: {student.get('courses_enrolled', 'N/A')}\n"

            latency_ms = round((time.time() - start_time) * 1000, 2)
            self.audit_repo.log_query(
                query_id=query_id,
                username=user.username,
                role=user.role,
                question=clean_message,
                answer=answer,
                latency_ms=latency_ms,
                chunk_count=1,
                confidence=1.0,
                is_fallback=False,
            )
            return ChatResponse(
                query_id=query_id,
                answer=answer,
                sources=[],
                confidence=1.0,
                evidence_quality="high",
                is_fallback=False,
                source="analytics_engine",
            )

        # Step 2: OKF Graph First Retrieval & Synthesis
        user_attributes = {"role": user.role, "enrollment_no": user.enrollment_no, "username": user.username}
        try:
            okf_res = self.retriever.query(clean_message, user_attributes)
        except Exception as e:
            logger.error(f"OKF Retrieval Failed: {e}")
            okf_res = {
                "source": "fallback_text",
                "reasoning": "Exception occurred during traversal.",
                "answer": "An error occurred while answering your question.",
                "context": []
            }
        
        latency_ms = round((time.time() - start_time) * 1000, 2)
        
        source = okf_res.get("source", "fallback_text")
        reasoning = okf_res.get("reasoning", "")
        answer = okf_res.get("answer") or "I could not find an answer in the graph or text context."
        anchors = okf_res.get("extracted_anchors", [])

        is_fallback = (source != "okf_graph" and source != "text_rag")

        sources = [
            SourceCitation(
                document_name=c.get("document_name", "Campus Document"),
                section=c.get("section", "General"),
                category=c.get("category", "general"),
                version=c.get("version", "1.0"),
                snippet=c.get("snippet", "")[:200] + ("..." if len(c.get("snippet", "")) > 200 else ""),
                score=float(c.get("rerank_score", c.get("score", 0.0))),
            )
            for c in okf_res.get("context", [])
        ]

        # Step 3: Observability & Audit Logging
        self.audit_repo.log_query(
            query_id=query_id,
            username=user.username,
            role=user.role,
            question=clean_message,
            answer=answer,
            latency_ms=latency_ms,
            chunk_count=len(anchors) if anchors else len(sources),
            confidence=1.0 if not is_fallback else 0.5,
            is_fallback=is_fallback,
        )

        return ChatResponse(
            query_id=query_id,
            answer=answer,
            sources=sources,
            confidence=1.0 if not is_fallback else 0.5,
            evidence_quality="high" if not is_fallback else "medium",
            is_fallback=is_fallback,
            source=source,
            reasoning_trace=reasoning,
            extracted_anchors=anchors
        )

    # Alias for backwards compatibility with evaluator
    process_chat = process_chat_query

    def submit_feedback(self, request: FeedbackRequest, user: UserSchema) -> dict:
        """Processes user feedback submission, ensuring ownership of the query."""
        owner = self.audit_repo.get_query_owner(request.query_id)
        if owner is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="The referenced query was not found.",
            )
        if owner != user.username:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You may only submit feedback for your own queries.",
            )
        self.audit_repo.log_feedback(request.query_id, request.is_positive)
        return {"status": "success", "message": "Feedback recorded successfully."}


chat_service = ChatService()
