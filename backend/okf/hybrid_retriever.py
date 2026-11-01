from typing import Dict, Any, List, Optional
from core.logging import logger
from okf.graph_agent import OKFGraphAgent

class OKFHybridRetriever:
    def __init__(self):
        self.graph_agent = OKFGraphAgent()
        
    def query(self, query: str, user_attributes: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Routes the query. Tries OKF Graph Agent first. 
        Falls back to legacy text retriever if no answer is generated (e.g. zero entities or traversal failure).
        """
        if user_attributes is None:
            user_attributes = {"role": "all"}
            
        logger.info(f"Routing query to OKF Graph Agent: {query}")
        anchors = self.graph_agent.extract_anchors(query)
        graph_response = self.graph_agent.answer_query(query) if anchors else None
        
        if graph_response:
            return {
                "source": "okf_graph",
                "reasoning": graph_response.reasoning,
                "answer": graph_response.answer,
                "context": [], # Graph context already synthesized in answer
                "extracted_anchors": anchors
            }
            
        logger.info("Graph Agent returned no entities or failed to answer. Executing graceful text fallback hook.")
        
        try:
            from rag.retriever import get_retriever
            retriever = get_retriever()
            role = user_attributes.get("role", "student")
            chunks, max_confidence = retriever.retrieve_chunks(query, user_role=role)
            if chunks:
                snippets = [c.get("snippet", "") for c in chunks if c.get("snippet")]
                answer = "\n\n".join(snippets)
                return {
                    "source": "text_rag",
                    "reasoning": f"Retrieved {len(chunks)} institutional document chunks from text database.",
                    "answer": answer,
                    "context": chunks,
                    "extracted_anchors": [],
                    "confidence": max_confidence,
                }
        except Exception as e:
            logger.warning(f"Fallback text retrieval error: {e}")
            
        return {
            "source": "fallback_text",
            "reasoning": "Entities not found in graph and no matching document chunks in text database.",
            "answer": "I don't have information on that in the official campus database.",
            "context": [],
            "extracted_anchors": []
        }
