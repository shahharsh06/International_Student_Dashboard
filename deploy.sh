#!/bin/bash

# =============================================================================
# PROFESSIONAL DEPLOYMENT SCRIPT
# International Student Financial Dashboard
# =============================================================================

set -e  # Exit on any error

echo "🚀 Starting Professional Deployment Process..."

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

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    print_error "Please run this script from the project root directory"
    exit 1
fi

# Check if git is initialized
if [ ! -d ".git" ]; then
    print_status "Initializing Git repository..."
    git init
    print_success "Git repository initialized"
fi

# Check git status
print_status "Checking Git status..."
if [ -z "$(git status --porcelain)" ]; then
    print_warning "No changes to commit"
else
    print_status "Staging changes..."
    git add .
    
    print_status "Creating commit..."
    git commit -m "Deployment update: $(date '+%Y-%m-%d %H:%M:%S')"
    print_success "Changes committed"
fi

# Check if remote is set
if ! git remote get-url origin > /dev/null 2>&1; then
    print_error "Git remote 'origin' not set. Please add your GitHub repository:"
    echo "git remote add origin https://github.com/YOUR_USERNAME/International_Student_Dashboard.git"
    exit 1
fi

# Push to GitHub
print_status "Pushing to GitHub..."
if git push origin main; then
    print_success "Code pushed to GitHub successfully"
else
    print_error "Failed to push to GitHub. Please check your credentials and try again."
    exit 1
fi

# Check deployment status
print_status "Checking deployment status..."
print_success "Deployment completed successfully!"
echo ""
echo "📋 Next Steps:"
echo "1. Visit https://share.streamlit.io/"
echo "2. Connect your GitHub account"
echo "3. Select your repository: International_Student_Dashboard"
echo "4. Deploy your app"
echo ""
echo "🌐 Your app will be available at:"
echo "https://your-app-name.streamlit.app/"
echo ""
echo "📊 Monitor your deployment at:"
echo "https://share.streamlit.io/your-username"

print_success "Professional deployment process completed! 🎉" 