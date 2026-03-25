"""Tests for PO lookup tools."""
import sys
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

from tools.po_lookup import get_po_status, search_delayed_pos, search_po_by_supplier


def test_get_po_status_found():
    """Test successful PO lookup."""
    result = get_po_status.invoke({"po_number": "PO-45001"})
    assert "PO-45001" in result
    assert "Marketing Materials" in result
    assert "ABC Printing Co." in result


def test_get_po_status_not_found():
    """Test PO lookup with non-existent PO."""
    result = get_po_status.invoke({"po_number": "PO-99999"})
    assert "not found" in result


def test_get_po_status_delayed():
    """Test PO lookup for delayed order."""
    result = get_po_status.invoke({"po_number": "PO-45003"})
    assert "PO-45003" in result
    assert "Delayed" in result
    assert "Delay Reason" in result


def test_search_delayed_pos():
    """Test search for delayed POs."""
    result = search_delayed_pos.invoke({})
    assert "PO-45003" in result
    assert "Delayed" in result


def test_search_po_by_supplier_found():
    """Test search by supplier name."""
    result = search_po_by_supplier.invoke({"supplier_name": "ABC Printing"})
    assert "PO-45001" in result
    assert "ABC Printing Co." in result


def test_search_po_by_supplier_not_found():
    """Test search by non-existent supplier."""
    result = search_po_by_supplier.invoke({"supplier_name": "Unknown Supplier"})
    assert "No Purchase Orders found" in result


if __name__ == "__main__":
    test_get_po_status_found()
    test_get_po_status_not_found()
    test_get_po_status_delayed()
    test_search_delayed_pos()
    test_search_po_by_supplier_found()
    test_search_po_by_supplier_not_found()
    print("✅ All PO lookup tests passed!")
