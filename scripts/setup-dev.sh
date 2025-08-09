#!/bin/bash

# Professional Management System - Development Setup Script
# This script sets up the development environment

set -e

echo "🚀 Setting up Professional Management System - Development Environment"
echo "=================================================================="

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

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    print_error "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    print_error "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create necessary directories
print_status "Creating necessary directories..."
mkdir -p data logs ssl frontend

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    print_status "Creating .env file from template..."
    cp .env.example .env
    print_warning "Please review and update the .env file with your configuration"
fi

# Create data directory and set permissions
print_status "Setting up data directory..."
mkdir -p data
chmod 755 data

# Create logs directory
print_status "Setting up logs directory..."
mkdir -p logs
chmod 755 logs

# Install Python dependencies locally (for development)
if [ -f requirements.txt ]; then
    print_status "Installing Python dependencies..."
    if command -v python3 &> /dev/null; then
        python3 -m pip install --user -r requirements.txt
        print_success "Python dependencies installed"
    else
        print_warning "Python3 not found. Dependencies will be installed in Docker container."
    fi
fi

# Run database migrations
print_status "Running database migrations..."
if command -v alembic &> /dev/null; then
    alembic upgrade head
    print_success "Database migrations completed"
else
    print_warning "Alembic not found locally. Migrations will run in Docker container."
fi

# Build and start development containers
print_status "Building and starting development containers..."
docker-compose -f docker-compose.dev.yml build
docker-compose -f docker-compose.dev.yml up -d

# Wait for services to be ready
print_status "Waiting for services to be ready..."
sleep 10

# Check if API is responding
print_status "Checking API health..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    print_success "API is running and healthy"
else
    print_warning "API might still be starting up. Check logs with: docker-compose -f docker-compose.dev.yml logs api"
fi

# Display useful information
echo ""
echo "=================================================================="
print_success "Development environment setup complete!"
echo ""
echo "📋 Services:"
echo "   • API: http://localhost:8000"
echo "   • API Docs: http://localhost:8000/docs"
echo "   • Health Check: http://localhost:8000/health"
echo "   • PostgreSQL: localhost:5433 (if needed)"
echo "   • Redis: localhost:6380 (if needed)"
echo ""
echo "🛠️  Useful commands:"
echo "   • View logs: docker-compose -f docker-compose.dev.yml logs -f"
echo "   • Stop services: docker-compose -f docker-compose.dev.yml down"
echo "   • Restart API: docker-compose -f docker-compose.dev.yml restart api"
echo "   • Run tests: docker-compose -f docker-compose.dev.yml exec api pytest"
echo "   • Access API container: docker-compose -f docker-compose.dev.yml exec api bash"
echo ""
echo "📁 Important files:"
echo "   • Environment: .env"
echo "   • Database: ./data/professional_management_dev.db"
echo "   • Logs: ./logs/"
echo ""
print_warning "Remember to update the .env file with your specific configuration!"
echo "=================================================================="

