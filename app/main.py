# Now safe to import AI frameworks and other dependencies
import logging
import os

import click
import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill

from agent_executor import AgentExecutor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", "5000"))


@click.command()
@click.option("--host", default=HOST)
@click.option("--port", default=PORT)
def main(host: str, port: int):
    skill = AgentSkill(
        id="procurement-status-inquiry",
        name="Procurement Status Inquiry",
        description="Check real-time status of Purchase Requisitions, Purchase Orders, and Invoices across SAP systems.",
        tags=["procurement", "purchase-order", "invoice", "status", "sap"],
        examples=[
            "What's the status of PO 4500012345?",
            "Show me my pending purchase requisitions",
            "Check invoice status for supplier ABC Corp",
            "Are there any delayed POs this week?",
            "What's the payment status for invoice 9000123456?",
        ],
    )
    agent_card = AgentCard(
        name="Procurement Status Chatbot",
        description="AI-powered chatbot providing real-time status information for PRs, POs, and Invoices across your procurement-to-pay process.",
        url=os.environ.get("AGENT_PUBLIC_URL", f"http://{host}:{port}/"),
        version="1.0.0",
        defaultInputModes=["text", "text/plain"],
        defaultOutputModes=["text", "text/plain"],
        capabilities=AgentCapabilities(streaming=True, pushNotifications=False),
        skills=[skill],
    )
    server = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=DefaultRequestHandler(
            agent_executor=AgentExecutor(),
            task_store=InMemoryTaskStore(),
        ),
    )
    logger.info(f"Starting Procurement Status Chatbot at http://{host}:{port}")
    uvicorn.run(server.build(), host=host, port=port)


if __name__ == "__main__":
    main()
