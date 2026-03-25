# Procurement Status Chatbot

An AI-powered chatbot that provides real-time status information for Purchase Requisitions (PRs), Purchase Orders (POs), and Invoices across your procurement-to-pay process.

## Overview

This agent enables self-service access to procurement data for:
- **Procurement specialists** - Track orders and respond to supplier inquiries
- **Finance team members** - Monitor invoice status and payment processing
- **Warehouse staff** - Check PO details for incoming deliveries
- **Internal requesters** - Track status of requested items

Built with:
- **A2A Protocol**: For agent-to-agent communication
- **LangGraph**: For agent orchestration
- **LiteLLM**: For model abstraction
- **Application Foundation SDK**: For SAP AI Core integration

## Features

- Natural language queries for PR, PO, and Invoice status
- Multi-system integration (S/4HANA, ECC, Ariba)
- Role-based access control
- Real-time data retrieval
- 24/7 availability

## Project Structure

- `app.yaml` - App Foundation workload configuration
- `Dockerfile` - Container build configuration
- `app/main.py` - A2A server entry point
- `app/agent_executor.py` - Request handling
- `app/agent.py` - Core agent logic with procurement tools
- `app/tools/` - Procurement-specific tools (PR, PO, Invoice lookup)

## Local Development

Running locally requires SAP Artifactory credentials and AI Core configuration due to internal SDK dependencies.

**For detailed local development instructions, use the `appfnd-agent-run-local` skill.**

## Example Queries

- "What's the status of PO 4500012345?"
- "Show me my pending purchase requisitions"
- "Check invoice status for supplier XYZ"
- "Are there any delayed POs this week?"
- "What's the payment status for invoice 9000123456?"
