# Vercel Deployment Guide

## Issues Fixed

The original deployment was failing because:
1. **Read-only file system**: Vercel's serverless environment doesn't allow writing to the local file system
2. **SQLite database**: Local SQLite files don't work in serverless environments
3. **Instance directory creation**: Flask-SQLAlchemy was trying to create directories

## Changes Made

### 1. Updated Configuration (`config.py`)
- Changed database configuration to use environment variables
- Added support for cloud databases (PostgreSQL, MySQL, etc.)
- Used in-memory SQLite for local development
- Added database engine options for better connection handling

### 2. Updated App Initialization (`app.py`)
- Added database initialization error handling
- Prevented duplicate initialization with global flag
- Added `@app.before_first_request` decorator for proper initialization
- Only add test data in local development environment

### 3. Updated Vercel Configuration (`vercel.json`)
- Changed entry point to `api/index.py` (Vercel best practice)
- Added function timeout configuration
- Added environment variable for SECRET_KEY

### 4. Updated API Entry Point (`api/index.py`)
- Added proper database initialization
- Added error handling for database setup

## Deployment Steps

### Option 1: Use Vercel Postgres (Recommended)

1. **Install Vercel CLI** (if not already installed):
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Create Vercel Postgres Database**:
   ```bash
   vercel postgres create
   ```

4. **Link your project**:
   ```bash
   vercel link
   ```

5. **Set environment variables**:
   ```bash
   vercel env add DATABASE_URL
   # Paste your Postgres connection string when prompted
   
   vercel env add SECRET_KEY
   # Enter a secure secret key when prompted
   ```

6. **Deploy**:
   ```bash
   vercel --prod
   ```

### Option 2: Use External Database

1. **Set up your database** (PostgreSQL, MySQL, etc.) on any cloud provider
2. **Get the connection string** in the format:
   - PostgreSQL: `postgresql://username:password@host:port/database`
   - MySQL: `mysql://username:password@host:port/database`

3. **Set environment variables in Vercel dashboard**:
   - Go to your project settings on vercel.com
   - Navigate to Environment Variables
   - Add `DATABASE_URL` with your connection string
   - Add `SECRET_KEY` with a secure random string

4. **Deploy**:
   ```bash
   vercel --prod
   ```

## Environment Variables Required

- `DATABASE_URL`: Your database connection string
- `SECRET_KEY`: A secure secret key for Flask sessions

## Database Schema

The app will automatically create the required tables:
- `course`: Stores course information
- `survey`: Stores survey responses

## Testing

After deployment:
1. Visit your Vercel URL
2. You should see the course list (initially empty in production)
3. Add courses through the admin interface or database directly
4. Test the survey functionality

## Troubleshooting

### If you get database connection errors:
1. Check that `DATABASE_URL` is correctly set
2. Verify your database is accessible from the internet
3. Check database credentials and permissions

### If you get import errors:
1. Make sure all dependencies are in `requirements.txt`
2. Check that the Python version is compatible

### For local development:
```bash
python app.py
```
This will use in-memory SQLite with test data.
