"""Purchase Order (PO) lookup tool."""
import logging
from typing import Optional

from langchain_core.tools import tool

logger = logging.getLogger(__name__)

# Mock data for demonstration - In production, this would call SAP APIs
MOCK_PO_DATA = {
    "PO-45001": {
        "number": "PO-45001",
        "description": "Marketing Materials",
        "status": "Goods Received",
        "supplier": "ABC Printing Co.",
        "created_date": "2024-01-09",
        "delivery_date": "2024-01-15",
        "total_amount": "3,500.00 USD",
        "buyer": "Lisa Anderson",
        "items": 8,
        "pr_number": "PR-10003",
    },
    "PO-45002": {
        "number": "PO-45002",
        "description": "IT Equipment",
        "status": "In Transit",
        "supplier": "Tech Solutions Inc.",
        "created_date": "2024-01-11",
        "delivery_date": "2024-01-20",
        "total_amount": "15,000.00 USD",
        "buyer": "James Wilson",
        "items": 3,
    },
    "PO-45003": {
        "number": "PO-45003",
        "description": "Office Furniture",
        "status": "Delayed",
        "supplier": "Office Depot",
        "created_date": "2024-01-05",
        "delivery_date": "2024-01-18",
        "expected_delivery": "2024-01-25",
        "total_amount": "8,750.00 USD",
        "buyer": "Lisa Anderson",
        "items": 12,
        "delay_reason": "Supplier production delay",
    },
}


@tool
def get_po_status(po_number: str) -> str:
    """Look up the status of a Purchase Order (PO).
    
    Args:
        po_number: The purchase order number (e.g., 'PO-45001' or '45001')
    
    Returns:
        A formatted string with PO status information
    """
    # Normalize PO number
    if not po_number.startswith("PO-"):
        po_number = f"PO-{po_number}"
    
    logger.info(f"Looking up PO: {po_number}")
    
    po = MOCK_PO_DATA.get(po_number)
    if not po:
        return f"Purchase Order {po_number} not found. Please verify the PO number and try again."
    
    result = f"""**Purchase Order Status**

📋 **PO Number:** {po['number']}
📝 **Description:** {po['description']}
🔄 **Status:** {po['status']}
🏢 **Supplier:** {po['supplier']}
👤 **Buyer:** {po['buyer']}
📅 **Created Date:** {po['created_date']}
🚚 **Delivery Date:** {po['delivery_date']}
💰 **Total Amount:** {po['total_amount']}
📦 **Items:** {po['items']}"""
    
    if po.get("pr_number"):
        result += f"\n🔗 **Related PR:** {po['pr_number']}"
    
    if po.get("delay_reason"):
        result += f"\n⚠️ **Delay Reason:** {po['delay_reason']}"
        result += f"\n📅 **Expected Delivery:** {po['expected_delivery']}"
    
    return result


@tool
def search_delayed_pos() -> str:
    """Search for all delayed Purchase Orders.
    
    Returns:
        A formatted string with delayed POs
    """
    logger.info("Searching for delayed POs")
    
    delayed = [po for po in MOCK_PO_DATA.values() if po['status'] == 'Delayed']
    
    if not delayed:
        return "No delayed Purchase Orders found. All POs are on track! ✅"
    
    result = "**Delayed Purchase Orders:**\n\n"
    for po in delayed:
        result += f"• **{po['number']}** - {po['description']}\n"
        result += f"  Supplier: {po['supplier']}\n"
        result += f"  Original Delivery: {po['delivery_date']}\n"
        result += f"  Expected Delivery: {po.get('expected_delivery', 'TBD')}\n"
        result += f"  Reason: {po.get('delay_reason', 'Unknown')}\n\n"
    
    return result


@tool
def search_po_by_supplier(supplier_name: str) -> str:
    """Search for Purchase Orders by supplier name.
    
    Args:
        supplier_name: The name of the supplier
    
    Returns:
        A formatted string with matching POs
    """
    logger.info(f"Searching POs for supplier: {supplier_name}")
    
    matches = [po for po in MOCK_PO_DATA.values() 
               if supplier_name.lower() in po['supplier'].lower()]
    
    if not matches:
        return f"No Purchase Orders found for supplier '{supplier_name}'."
    
    result = f"**Purchase Orders for {supplier_name}:**\n\n"
    for po in matches:
        result += f"• **{po['number']}** - {po['description']} - Status: {po['status']} - Amount: {po['total_amount']}\n"
    
    return result
