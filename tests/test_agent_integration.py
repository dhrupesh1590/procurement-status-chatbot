"""Integration test for the complete agent."""
import sys
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "app"))

from agent import ProcurementStatusAgent


def test_agent_pr_query():
    """Test agent with PR query."""
    agent = ProcurementStatusAgent()
    response = agent.invoke("What's the status of PR-10001?", "test-context")
    
    assert response.status == "completed"
    assert "PR-10001" in response.message
    print(f"✅ PR Query Response:\n{response.message}\n")


def test_agent_po_query():
    """Test agent with PO query."""
    agent = ProcurementStatusAgent()
    response = agent.invoke("Check PO-45003 status", "test-context")
    
    assert response.status == "completed"
    assert "PO-45003" in response.message
    print(f"✅ PO Query Response:\n{response.message}\n")


def test_agent_invoice_query():
    """Test agent with invoice query."""
    agent = ProcurementStatusAgent()
    response = agent.invoke("Show me invoice INV-9001", "test-context")
    
    assert response.status == "completed"
    assert "INV-9001" in response.message
    print(f"✅ Invoice Query Response:\n{response.message}\n")


def test_agent_search_query():
    """Test agent with search query."""
    agent = ProcurementStatusAgent()
    response = agent.invoke("Are there any delayed POs?", "test-context")
    
    assert response.status == "completed"
    print(f"✅ Search Query Response:\n{response.message}\n")


if __name__ == "__main__":
    print("Running integration tests...\n")
    test_agent_pr_query()
    test_agent_po_query()
    test_agent_invoice_query()
    test_agent_search_query()
    print("✅ All integration tests passed!")
