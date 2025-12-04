#!/bin/bash

echo "🚀 Deploying Trading Bot to Fly.io..."

# Check if flyctl is installed
if ! command -v flyctl &> /dev/null; then
    echo "❌ Fly.io CLI (flyctl) is not installed."
    echo "📥 Installing flyctl..."
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        if command -v brew &> /dev/null; then
            brew install flyctl
        else
            curl -L https://fly.io/install.sh | sh
            echo "⚠️  Please add flyctl to your PATH and run this script again"
            echo "   Add this to your ~/.zshrc or ~/.bash_profile:"
            echo "   export FLYCTL_INSTALL=\"$HOME/.fly\""
            echo "   export PATH=\"\$FLYCTL_INSTALL/bin:\$PATH\""
            exit 1
        fi
    else
        curl -L https://fly.io/install.sh | sh
        echo "⚠️  Please add flyctl to your PATH and run this script again"
        exit 1
    fi
fi

echo "✅ Fly.io CLI found"

# Login check
if ! flyctl auth whoami &> /dev/null; then
    echo "🔐 Please login to Fly.io..."
    flyctl auth login
fi

echo "✅ Logged in to Fly.io"

# Check if app exists
if flyctl status &> /dev/null; then
    echo "📦 App exists, deploying update..."
    flyctl deploy
else
    echo "🆕 Creating new app..."
    flyctl launch --now
fi

echo "✅ Deployment complete!"
echo ""
echo "📊 Useful commands:"
echo "  flyctl logs          - View logs"
echo "  flyctl status        - Check status"
echo "  flyctl open          - Open in browser"
echo "  flyctl ssh console   - SSH into machine"
