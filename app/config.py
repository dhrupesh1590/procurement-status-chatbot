"""Agent configuration exposed via lowcode decorators."""
from lowcode.decorators import agent_config, prompt_section
from lowcode.registry import GroupKind


# Agent Configuration
@agent_config(
    key="agent.model",
    label="LLM Model",
    description="The LLM model identifier for SAP AI Core",
    group=GroupKind.BASICS,
    order=0
)
def model_name():
    return "sap/anthropic--claude-4.5-sonnet"


@agent_config(
    key="agent.temperature",
    label="Temperature",
    description="Sampling temperature for LLM responses (0.0 = deterministic, 1.0 = creative)",
    group=GroupKind.ADVANCED,
    order=1
)
def temperature():
    return 0.7


@agent_config(
    key="agent.max_iterations",
    label="Max Iterations",
    description="Maximum number of tool call iterations before stopping",
    group=GroupKind.ADVANCED,
    order=2
)
def max_iterations():
    return 10


# Prompt Sections
@prompt_section(
    key="prompts.system",
    label="System Prompt",
    description="Main system prompt defining agent behavior and capabilities",
    group=GroupKind.BASICS,
    order=0
)
def system_prompt():
    return """You are a Procurement Status Assistant helping users check the status of Purchase Requisitions (PRs), Purchase Orders (POs), and Invoices.

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


@prompt_section(
    key="prompts.greeting",
    label="Greeting Message",
    description="Initial greeting message when users first interact with the agent",
    group=GroupKind.BASICS,
    order=1
)
def greeting_prompt():
    return """Hello! I'm your Procurement Status Assistant. I can help you check the status of:
- Purchase Requisitions (PRs)
- Purchase Orders (POs)
- Invoices

Just ask me about any document by number, or ask general questions like "show delayed POs" or "any overdue invoices?"

How can I help you today?"""


# Feature Flags
@agent_config(
    key="features.enable_pr_lookup",
    label="Enable PR Lookup",
    description="Enable Purchase Requisition lookup functionality",
    group=GroupKind.EXPERT,
    order=10
)
def enable_pr_lookup():
    return True


@agent_config(
    key="features.enable_po_lookup",
    label="Enable PO Lookup",
    description="Enable Purchase Order lookup functionality",
    group=GroupKind.EXPERT,
    order=11
)
def enable_po_lookup():
    return True


@agent_config(
    key="features.enable_invoice_lookup",
    label="Enable Invoice Lookup",
    description="Enable Invoice lookup functionality",
    group=GroupKind.EXPERT,
    order=12
)
def enable_invoice_lookup():
    return True
