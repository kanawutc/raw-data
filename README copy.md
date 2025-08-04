# Database Explorer - Cloud Ready

A lightweight web-based database explorer for managing CSV data with full CRUD operations, ready for deployment on Render.com.

## 🚀 Quick Deploy to Render.com

1. **Setup Git Repository**
   ```bash
   ./setup_git.sh
   ```

2. **Push to GitHub**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/database-explorer.git
   git push -u origin main
   ```

3. **Deploy on Render**
   - Go to [render.com](https://render.com)
   - Connect your GitHub repository
   - Render will auto-detect `render.yaml`
   - Click Deploy!

## 📋 Features

- **5 Database Tables**: Domain Cost, Hosting Cost, Performance, Revenue, Salary
- **Full CRUD Operations**: Create, Read, Update, Delete
- **CSV Import**: Upload and import your data
- **SQLite Database**: Persistent cloud storage
- **Responsive Design**: Works on all devices
- **Health Monitoring**: Built-in health checks

## 🧪 Test Locally

```bash
./start_render_local.sh
```
Then visit: http://localhost:8000

## 📁 Files Included

- `app.py` - Main Flask application
- `requirements.txt` - Python dependencies  
- `render.yaml` - Render configuration
- `templates/` - HTML templates
- `Sample Data - *.csv` - Your original CSV files
- `database_explorer.db` - SQLite database with your data

## 📖 Full Documentation

See `RENDER_DEPLOYMENT.md` for complete deployment guide and troubleshooting.

## 🎯 Your Data

Your original CSV data is stored in the SQLite database and ready to use. The app includes sample data and full CSV import functionality.# raw-data
