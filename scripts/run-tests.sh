#!/bin/bash

# Professional Management System - Test Runner Script
# This script runs all tests with coverage reporting

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

echo "🧪 Running Professional Management System Tests"
echo "=============================================="

# Default values
TEST_TYPE="all"
COVERAGE=true
VERBOSE=false
DOCKER=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -t|--type)
            TEST_TYPE="$2"
            shift 2
            ;;
        --no-coverage)
            COVERAGE=false
            shift
            ;;
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -d|--docker)
            DOCKER=true
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  -t, --type TYPE     Test type: all, unit, integration (default: all)"
            echo "  --no-coverage       Disable coverage reporting"
            echo "  -v, --verbose       Verbose output"
            echo "  -d, --docker        Run tests in Docker container"
            echo "  -h, --help          Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                  # Run all tests with coverage"
            echo "  $0 -t unit          # Run only unit tests"
            echo "  $0 -d               # Run tests in Docker"
            echo "  $0 --no-coverage    # Run tests without coverage"
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Build pytest command
PYTEST_CMD="python -m pytest"

# Add test path based on type
case $TEST_TYPE in
    unit)
        PYTEST_CMD="$PYTEST_CMD tests/unit/"
        ;;
    integration)
        PYTEST_CMD="$PYTEST_CMD tests/integration/"
        ;;
    all)
        PYTEST_CMD="$PYTEST_CMD tests/"
        ;;
    *)
        print_error "Invalid test type: $TEST_TYPE. Use: all, unit, integration"
        exit 1
        ;;
esac

# Add coverage if enabled
if [ "$COVERAGE" = true ]; then
    PYTEST_CMD="$PYTEST_CMD --cov=. --cov-report=html --cov-report=term-missing --cov-report=xml"
fi

# Add verbose if enabled
if [ "$VERBOSE" = true ]; then
    PYTEST_CMD="$PYTEST_CMD -v"
fi

# Add other pytest options
PYTEST_CMD="$PYTEST_CMD --tb=short"

print_status "Test configuration:"
echo "  • Test type: $TEST_TYPE"
echo "  • Coverage: $COVERAGE"
echo "  • Verbose: $VERBOSE"
echo "  • Docker: $DOCKER"
echo ""

# Run tests
if [ "$DOCKER" = true ]; then
    print_status "Running tests in Docker container..."
    
    # Check if container is running
    if ! docker-compose -f docker-compose.dev.yml ps api | grep -q "Up"; then
        print_status "Starting development containers..."
        docker-compose -f docker-compose.dev.yml up -d api
        sleep 5
    fi
    
    # Run tests in container
    docker-compose -f docker-compose.dev.yml exec -T api $PYTEST_CMD
    
else
    print_status "Running tests locally..."
    
    # Check if virtual environment exists
    if [ -d "venv" ]; then
        print_status "Activating virtual environment..."
        source venv/bin/activate
    fi
    
    # Check if dependencies are installed
    if ! python -c "import pytest" 2>/dev/null; then
        print_status "Installing test dependencies..."
        pip install -r requirements.txt
    fi
    
    # Run tests
    $PYTEST_CMD
fi

# Check test results
if [ $? -eq 0 ]; then
    print_success "All tests passed! ✅"
    
    if [ "$COVERAGE" = true ]; then
        echo ""
        print_status "Coverage report generated:"
        echo "  • HTML: htmlcov/index.html"
        echo "  • XML: coverage.xml"
        
        # Open coverage report if running locally and not in CI
        if [ "$DOCKER" = false ] && [ -z "$CI" ] && command -v xdg-open &> /dev/null; then
            print_status "Opening coverage report in browser..."
            xdg-open htmlcov/index.html 2>/dev/null || true
        fi
    fi
    
else
    print_error "Some tests failed! ❌"
    exit 1
fi

echo ""
echo "=============================================="
print_success "Test execution completed!"

