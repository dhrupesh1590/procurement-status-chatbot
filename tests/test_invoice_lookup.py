"""Tests for Invoice lookup tools."""
import sys
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

from tools.invoice_lookup import (
    get_invoice_status,
    search_invoice_by_supplier,
    search_overdue_invoices,
    search_blocked_invoices,
)


def test_get_invoice_status_found():
    """Test successful invoice lookup."""
    result = get_invoice_status.invoke({"invoice_number": "INV-9001"})
    assert "INV-9001" in result
    assert "Marketing Materials Invoice" in result
    assert "Paid" in result


def test_get_invoice_status_not_found():
    """Test invoice lookup with non-existent invoice."""
    result = get_invoice_status.invoke({"invoice_number": "INV-99999"})
    assert "not found" in result


def test_get_invoice_status_blocked():
    """Test invoice lookup for blocked invoice."""
    result = get_invoice_status.invoke({"invoice_number": "INV-9003"})
    assert "INV-9003" in result
    assert "Blocked" in result
    assert "Block Reason" in result


def test_search_invoice_by_supplier_found():
    """Test search by supplier name."""
    result = search_invoice_by_supplier.invoke({"supplier_name": "ABC Printing"})
    assert "INV-9001" in result
    assert "ABC Printing Co." in result


def test_search_invoice_by_supplier_not_found():
    """Test search by non-existent supplier."""
    result = search_invoice_by_supplier.invoke({"supplier_name": "Unknown Supplier"})
    assert "No Invoices found" in result


def test_search_overdue_invoices():
    """Test search for overdue invoices."""
    result = search_overdue_invoices.invoke({})
    assert "INV-9004" in result
    assert "Overdue" in result


def test_search_blocked_invoices():
    """Test search for blocked invoices."""
    result = search_blocked_invoices.invoke({})
    assert "INV-9003" in result
    assert "Blocked" in result


if __name__ == "__main__":
    test_get_invoice_status_found()
    test_get_invoice_status_not_found()
    test_get_invoice_status_blocked()
    test_search_invoice_by_supplier_found()
    test_search_invoice_by_supplier_not_found()
    test_search_overdue_invoices()
    test_search_blocked_invoices()
    print("✅ All Invoice lookup tests passed!")
