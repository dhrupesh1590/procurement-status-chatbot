"""Invoice lookup tool."""
import logging
from typing import Optional

from langchain_core.tools import tool

logger = logging.getLogger(__name__)

# Mock data for demonstration - In production, this would call SAP APIs
MOCK_INVOICE_DATA = {
    "INV-9001": {
        "number": "INV-9001",
        "description": "Marketing Materials Invoice",
        "status": "Paid",
        "supplier": "ABC Printing Co.",
        "invoice_date": "2024-01-16",
        "due_date": "2024-02-15",
        "payment_date": "2024-01-30",
        "total_amount": "3,500.00 USD",
        "po_number": "PO-45001",
    },
    "INV-9002": {
        "number": "INV-9002",
        "description": "IT Equipment Invoice",
        "status": "Pending Payment",
        "supplier": "Tech Solutions Inc.",
        "invoice_date": "2024-01-20",
        "due_date": "2024-02-19",
        "total_amount": "15,000.00 USD",
        "po_number": "PO-45002",
        "approval_stage": "Approved - Awaiting Payment Run",
    },
    "INV-9003": {
        "number": "INV-9003",
        "description": "Office Furniture Invoice",
        "status": "Blocked",
        "supplier": "Office Depot",
        "invoice_date": "2024-01-22",
        "due_date": "2024-02-21",
        "total_amount": "8,750.00 USD",
        "po_number": "PO-45003",
        "block_reason": "Price variance - invoice amount exceeds PO by 5%",
    },
    "INV-9004": {
        "number": "INV-9004",
        "description": "Consulting Services",
        "status": "Overdue",
        "supplier": "Business Consultants LLC",
        "invoice_date": "2023-12-15",
        "due_date": "2024-01-14",
        "total_amount": "12,000.00 USD",
        "days_overdue": 15,
    },
}


@tool
def get_invoice_status(invoice_number: str) -> str:
    """Look up the status of an Invoice.
    
    Args:
        invoice_number: The invoice number (e.g., 'INV-9001' or '9001')
    
    Returns:
        A formatted string with invoice status information
    """
    # Normalize invoice number
    if not invoice_number.startswith("INV-"):
        invoice_number = f"INV-{invoice_number}"
    
    logger.info(f"Looking up Invoice: {invoice_number}")
    
    invoice = MOCK_INVOICE_DATA.get(invoice_number)
    if not invoice:
        return f"Invoice {invoice_number} not found. Please verify the invoice number and try again."
    
    result = f"""**Invoice Status**

📋 **Invoice Number:** {invoice['number']}
📝 **Description:** {invoice['description']}
🔄 **Status:** {invoice['status']}
🏢 **Supplier:** {invoice['supplier']}
📅 **Invoice Date:** {invoice['invoice_date']}
📅 **Due Date:** {invoice['due_date']}
💰 **Total Amount:** {invoice['total_amount']}"""
    
    if invoice.get("po_number"):
        result += f"\n🔗 **Related PO:** {invoice['po_number']}"
    
    if invoice.get("payment_date"):
        result += f"\n✅ **Payment Date:** {invoice['payment_date']}"
    
    if invoice.get("approval_stage"):
        result += f"\n⏳ **Approval Stage:** {invoice['approval_stage']}"
    
    if invoice.get("block_reason"):
        result += f"\n🚫 **Block Reason:** {invoice['block_reason']}"
    
    if invoice.get("days_overdue"):
        result += f"\n⚠️ **Days Overdue:** {invoice['days_overdue']}"
    
    return result


@tool
def search_invoice_by_supplier(supplier_name: str) -> str:
    """Search for Invoices by supplier name.
    
    Args:
        supplier_name: The name of the supplier
    
    Returns:
        A formatted string with matching invoices
    """
    logger.info(f"Searching invoices for supplier: {supplier_name}")
    
    matches = [inv for inv in MOCK_INVOICE_DATA.values() 
               if supplier_name.lower() in inv['supplier'].lower()]
    
    if not matches:
        return f"No Invoices found for supplier '{supplier_name}'."
    
    result = f"**Invoices for {supplier_name}:**\n\n"
    for inv in matches:
        result += f"• **{inv['number']}** - {inv['description']} - Status: {inv['status']} - Amount: {inv['total_amount']}\n"
    
    return result


@tool
def search_overdue_invoices() -> str:
    """Search for all overdue invoices.
    
    Returns:
        A formatted string with overdue invoices
    """
    logger.info("Searching for overdue invoices")
    
    overdue = [inv for inv in MOCK_INVOICE_DATA.values() if inv['status'] == 'Overdue']
    
    if not overdue:
        return "No overdue invoices found. All payments are current! ✅"
    
    result = "**Overdue Invoices:**\n\n"
    for inv in overdue:
        result += f"• **{inv['number']}** - {inv['description']}\n"
        result += f"  Supplier: {inv['supplier']}\n"
        result += f"  Due Date: {inv['due_date']}\n"
        result += f"  Amount: {inv['total_amount']}\n"
        result += f"  Days Overdue: {inv.get('days_overdue', 'Unknown')}\n\n"
    
    return result


@tool
def search_blocked_invoices() -> str:
    """Search for all blocked invoices.
    
    Returns:
        A formatted string with blocked invoices
    """
    logger.info("Searching for blocked invoices")
    
    blocked = [inv for inv in MOCK_INVOICE_DATA.values() if inv['status'] == 'Blocked']
    
    if not blocked:
        return "No blocked invoices found. ✅"
    
    result = "**Blocked Invoices:**\n\n"
    for inv in blocked:
        result += f"• **{inv['number']}** - {inv['description']}\n"
        result += f"  Supplier: {inv['supplier']}\n"
        result += f"  Amount: {inv['total_amount']}\n"
        result += f"  Block Reason: {inv.get('block_reason', 'Unknown')}\n\n"
    
    return result
