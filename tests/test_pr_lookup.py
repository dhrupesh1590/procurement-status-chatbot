"""Tests for PR lookup tools."""
import sys
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

from tools.pr_lookup import get_pr_status, search_pr_by_requester


def test_get_pr_status_found():
    """Test successful PR lookup."""
    result = get_pr_status.invoke({"pr_number": "PR-10001"})
    assert "PR-10001" in result
    assert "Office Supplies" in result
    assert "Approved" in result
    assert "John Smith" in result


def test_get_pr_status_not_found():
    """Test PR lookup with non-existent PR."""
    result = get_pr_status.invoke({"pr_number": "PR-99999"})
    assert "not found" in result


def test_get_pr_status_without_prefix():
    """Test PR lookup without PR- prefix."""
    result = get_pr_status.invoke({"pr_number": "10001"})
    assert "PR-10001" in result
    assert "Office Supplies" in result


def test_search_pr_by_requester_found():
    """Test search by requester name."""
    result = search_pr_by_requester.invoke({"requester_name": "John Smith"})
    assert "PR-10001" in result
    assert "Office Supplies" in result


def test_search_pr_by_requester_not_found():
    """Test search by non-existent requester."""
    result = search_pr_by_requester.invoke({"requester_name": "Unknown Person"})
    assert "No Purchase Requisitions found" in result


if __name__ == "__main__":
    test_get_pr_status_found()
    test_get_pr_status_not_found()
    test_get_pr_status_without_prefix()
    test_search_pr_by_requester_found()
    test_search_pr_by_requester_not_found()
    print("✅ All PR lookup tests passed!")
