"""Procurement Status Agent - Core agent logic with LangGraph."""
import logging
import os
from dataclasses import dataclass
from typing import AsyncGenerator, Literal

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode

from tools.pr_lookup import get_pr_status, search_pr_by_requester
from tools.po_lookup import get_po_status, search_delayed_pos, search_po_by_supplier
from tools.invoice_lookup import (
    get_invoice_status,
    search_invoice_by_supplier,
    search_overdue_invoices,
    search_blocked_invoices,
)

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a Procurement Status Assistant helping users check the status of Purchase Requisitions (PRs), Purchase Orders (POs), and Invoices.

**Your capabilities:**
- Look up PR, PO, and Invoice status by document number
- Search for documents by requester, supplier, or other criteria
- Find delayed POs, overdue invoices, and blocked invoices
- Provide clear, formatted status information

**Guidelines:**
- Be friendly, professional, and concise
- When users provide document numbers, use the appropriate lookup tool
- Format responses clearly with relevant details
- If a document is not found, suggest checking the document number
- For general queries like "show my PRs" or "any delayed POs", use search tools
- Always provide actionable information

**Available Tools:**
- Purchase Requisitions: get_pr_status, search_pr_by_requester
- Purchase Orders: get_po_status, search_delayed_pos, search_po_by_supplier
- Invoices: get_invoice_status, search_invoice_by_supplier, search_overdue_invoices, search_blocked_invoices

Remember: You're here to make procurement status inquiries quick and easy!"""


@dataclass
class AgentResponse:
    status: Literal["input_required", "completed", "error"]
    message: str


class ProcurementStatusAgent:
    SUPPORTED_CONTENT_TYPES = ["text", "text/plain"]

    def __init__(self):
        # Use OpenAI-compatible endpoint - can be configured via environment
        api_key = os.getenv("OPENAI_API_KEY", "dummy-key-for-demo")
        base_url = os.getenv("OPENAI_BASE_URL", None)
        
        self.llm = ChatOpenAI(
            model=os.getenv("MODEL_NAME", "gpt-4o"),
            api_key=api_key,
            base_url=base_url,
            temperature=0.7
        )
        
        # Define all procurement tools
        self.tools = [
            # PR tools
            get_pr_status,
            search_pr_by_requester,
            # PO tools
            get_po_status,
            search_delayed_pos,
            search_po_by_supplier,
            # Invoice tools
            get_invoice_status,
            search_invoice_by_supplier,
            search_overdue_invoices,
            search_blocked_invoices,
        ]
        
        self.graph = self._build_graph()

    def _build_graph(self):
        """Build the LangGraph agent with tool calling capabilities."""
        
        # Bind tools to the LLM
        llm_with_tools = self.llm.bind_tools(self.tools)
        
        async def call_model(state: MessagesState):
            response = await llm_with_tools.ainvoke(state["messages"])
            return {"messages": [response]}
        
        def should_continue(state: MessagesState):
            """Determine if we should continue to tools or end."""
            last_message = state["messages"][-1]
            if hasattr(last_message, "tool_calls") and last_message.tool_calls:
                return "tools"
            return "end"
        
        # Build the graph
        builder = StateGraph(MessagesState)
        builder.add_node("model", call_model)
        builder.add_node("tools", ToolNode(self.tools))
        
        builder.add_edge(START, "model")
        builder.add_conditional_edges("model", should_continue, {"tools": "tools", "end": "__end__"})
        builder.add_edge("tools", "model")
        
        return builder.compile()

    async def stream(self, query: str, context_id: str) -> AsyncGenerator[dict, None]:
        """Stream agent responses."""
        yield {"is_task_complete": False, "require_user_input": False, "content": "Processing your request..."}
        
        try:
            messages = [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=query)
            ]
            
            result = await self.graph.ainvoke({"messages": messages})
            response = result["messages"][-1].content
            
            yield {"is_task_complete": True, "require_user_input": False, "content": response}
            
        except Exception as e:
            logger.exception("Error processing request")
            yield {
                "is_task_complete": True,
                "require_user_input": False,
                "content": f"I encountered an error processing your request: {str(e)}. Please try again or rephrase your question."
            }

    def invoke(self, query: str, context_id: str) -> AgentResponse:
        """Synchronous invoke method for testing."""
        import asyncio
        try:
            messages = [
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=query)
            ]
            
            result = asyncio.run(self.graph.ainvoke({"messages": messages}))
            response = result["messages"][-1].content
            
            return AgentResponse(status="completed", message=response)
            
        except Exception as e:
            logger.exception("Error processing request")
            return AgentResponse(
                status="error",
                message=f"Error: {str(e)}"
            )
