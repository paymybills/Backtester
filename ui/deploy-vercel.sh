#!/bin/bash

# Vercel Deployment Script
echo "🚀 Deploying Backtesting Engine to Vercel..."

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Please run this script from the ui/ directory"
    exit 1
fi

# Install Vercel CLI if not installed
if ! command -v vercel &> /dev/null; then
    echo "📦 Installing Vercel CLI..."
    npm install -g vercel
fi

# Build the project first
echo "🔨 Building the project..."
npm run build

# Deploy to Vercel
echo "🌐 Deploying to Vercel..."
vercel --prod

echo "✅ Deployment complete!"
echo ""
echo "📋 Next steps:"
echo "1. Set environment variables in Vercel dashboard:"
echo "   - VITE_API_URL: Your backend API URL"
echo "2. Configure custom domain (optional)"
echo "3. Test the deployed application"
echo ""
echo "🔗 Vercel Dashboard: https://vercel.com/dashboard"