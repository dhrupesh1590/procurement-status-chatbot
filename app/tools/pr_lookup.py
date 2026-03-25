"""Purchase Requisition (PR) lookup tool."""
import logging
from typing import Optional

from langchain_core.tools import tool

logger = logging.getLogger(__name__)

# Mock data for demonstration - In production, this would call SAP APIs
MOCK_PR_DATA = {
    "PR-10001": {
        "number": "PR-10001",
        "description": "Office Supplies",
        "status": "Approved",
        "requester": "John Smith",
        "created_date": "2024-01-10",
        "total_amount": "1,250.00 USD",
        "approval_stage": "Final Approval Complete",
        "items": 5,
    },
    "PR-10002": {
        "number": "PR-10002",
        "description": "IT Equipment",
        "status": "Pending Approval",
        "requester": "Sarah Johnson",
        "created_date": "2024-01-12",
        "total_amount": "15,000.00 USD",
        "approval_stage": "Awaiting Manager Approval",
        "items": 3,
    },
    "PR-10003": {
        "number": "PR-10003",
        "description": "Marketing Materials",
        "status": "Converted to PO",
        "requester": "Michael Brown",
        "created_date": "2024-01-08",
        "total_amount": "3,500.00 USD",
        "approval_stage": "Approved - PO Created",
        "items": 8,
        "po_number": "PO-45001",
    },
}


@tool
def get_pr_status(pr_number: str) -> str:
    """Look up the status of a Purchase Requisition (PR).
    
    Args:
        pr_number: The purchase requisition number (e.g., 'PR-10001' or '10001')
    
    Returns:
        A formatted string with PR status information
    """
    # Normalize PR number
    if not pr_number.startswith("PR-"):
        pr_number = f"PR-{pr_number}"
    
    logger.info(f"Looking up PR: {pr_number}")
    
    pr = MOCK_PR_DATA.get(pr_number)
    if not pr:
        return f"Purchase Requisition {pr_number} not found. Please verify the PR number and try again."
    
    result = f"""**Purchase Requisition Status**

📋 **PR Number:** {pr['number']}
📝 **Description:** {pr['description']}
🔄 **Status:** {pr['status']}
👤 **Requester:** {pr['requester']}
📅 **Created Date:** {pr['created_date']}
💰 **Total Amount:** {pr['total_amount']}
✅ **Approval Stage:** {pr['approval_stage']}
📦 **Items:** {pr['items']}"""
    
    if pr.get("po_number"):
        result += f"\n🔗 **Related PO:** {pr['po_number']}"
    
    return result


@tool
def search_pr_by_requester(requester_name: str) -> str:
    """Search for Purchase Requisitions by requester name.
    
    Args:
        requester_name: The name of the person who created the PR
    
    Returns:
        A formatted string with matching PRs
    """
    logger.info(f"Searching PRs for requester: {requester_name}")
    
    matches = [pr for pr in MOCK_PR_DATA.values() 
               if requester_name.lower() in pr['requester'].lower()]
    
    if not matches:
        return f"No Purchase Requisitions found for requester '{requester_name}'."
    
    result = f"**Purchase Requisitions for {requester_name}:**\n\n"
    for pr in matches:
        result += f"• **{pr['number']}** - {pr['description']} - Status: {pr['status']} - Amount: {pr['total_amount']}\n"
    
    return result
