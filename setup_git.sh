#!/bin/bash

echo "🔧 Setting up Git Repository for Render Deployment"
echo "=================================================="

# Initialize git if not already done
if [ ! -d ".git" ]; then
    echo "📦 Initializing Git repository..."
    git init
    git branch -M main
else
    echo "✅ Git repository already initialized"
fi

# Create .gitignore if it doesn't exist
if [ ! -f ".gitignore" ]; then
    echo "📝 Creating .gitignore..."
    cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
env.bak/
venv.bak/
.env

# Database
*.db-journal

# IDE
.vscode/
.DS_Store
*.swp
*.swo

# Logs
*.log

# Temporary files
*.tmp
*.temp
EOF
else
    echo "✅ .gitignore already exists"
fi

# Add files to git
echo "📁 Adding files to Git..."
git add .

# Check if there are changes to commit
if git diff --staged --quiet; then
    echo "✅ No changes to commit"
else
    echo "💾 Committing changes..."
    git commit -m "Refactor for Render.com deployment

- Add Render-compatible Flask app
- Configure gunicorn production server
- Add environment variable support
- Include health check endpoint
- Set up automatic database initialization
- Complete CRUD operations with CSV import
- Mobile responsive design"
fi

echo ""
echo "🌐 Next Steps:"
echo "1. Create a repository on GitHub"
echo "2. Run: git remote add origin https://github.com/YOUR_USERNAME/database-explorer.git"
echo "3. Run: git push -u origin main"
echo "4. Go to render.com and deploy from your GitHub repository"
echo ""
echo "🚀 Your files are ready for deployment!"