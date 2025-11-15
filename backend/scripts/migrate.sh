#!/bin/bash
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print usage
usage() {
    echo -e "${BLUE}Usage:${NC}"
    echo "  $0 <command> [options]"
    echo ""
    echo -e "${BLUE}Commands:${NC}"
    echo "  upgrade [revision]    Apply migrations (default: head)"
    echo "  downgrade [revision]  Rollback migrations (default: -1)"
    echo "  revision [message]    Create new migration with autogenerate"
    echo "  current               Show current migration version"
    echo "  history               Show migration history"
    echo "  show [revision]       Show migration details"
    echo ""
    echo -e "${BLUE}Examples:${NC}"
    echo "  $0 upgrade            # Apply all pending migrations"
    echo "  $0 downgrade -1       # Rollback one migration"
    echo "  $0 revision 'add users table'  # Create new migration"
    echo "  $0 current           # Show current version"
    echo "  $0 history           # Show all migrations"
}

# Check if command is provided
if [ $# -eq 0 ]; then
    usage
    exit 1
fi

COMMAND=$1
shift

case "$COMMAND" in
    upgrade)
        REVISION=${1:-head}
        echo -e "${YELLOW}Upgrading database to revision: ${REVISION}${NC}"
        alembic upgrade "$REVISION"
        echo -e "${GREEN}Migration upgrade completed${NC}"
        ;;
    
    downgrade)
        REVISION=${1:--1}
        echo -e "${YELLOW}Downgrading database to revision: ${REVISION}${NC}"
        alembic downgrade "$REVISION"
        echo -e "${GREEN}Migration downgrade completed${NC}"
        ;;
    
    revision)
        if [ -z "$1" ]; then
            echo -e "${RED}Error: Migration message is required${NC}"
            echo "Usage: $0 revision 'your migration message'"
            exit 1
        fi
        MESSAGE="$1"
        echo -e "${YELLOW}Creating new migration: ${MESSAGE}${NC}"
        alembic revision --autogenerate -m "$MESSAGE"
        echo -e "${GREEN}Migration file created${NC}"
        ;;
    
    current)
        echo -e "${YELLOW}Current migration version:${NC}"
        alembic current
        ;;
    
    history)
        echo -e "${YELLOW}Migration history:${NC}"
        alembic history
        ;;
    
    show)
        if [ -z "$1" ]; then
            echo -e "${RED}Error: Revision is required${NC}"
            echo "Usage: $0 show <revision>"
            exit 1
        fi
        echo -e "${YELLOW}Migration details for: $1${NC}"
        alembic show "$1"
        ;;
    
    *)
        echo -e "${RED}Unknown command: ${COMMAND}${NC}"
        echo ""
        usage
        exit 1
        ;;
esac

