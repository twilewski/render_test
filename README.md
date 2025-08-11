# Task Manager App

A simple full-stack application with Python Flask backend, Vue.js frontend, and MySQL database.

## Features

- Create, read, update, and delete tasks
- Mark tasks as complete/incomplete
- Responsive web interface
- MySQL database with automatic migrations

## Local Development

### Backend
```bash
pip install -r requirements.txt
python app.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Render Deployment

### Option 1: Using render.yaml (Recommended)

1. Push this code to a GitHub repository
2. Connect your GitHub repo to Render
3. Render will automatically detect the `render.yaml` file and create:
   - A MySQL database
   - A web service that builds and serves your app

### Option 2: Manual Setup

1. **Create a MySQL Database:**
   - Go to Render Dashboard → New → MySQL
   - Name: `taskmanager-db`
   - Note the connection string

2. **Create a Web Service:**
   - Go to Render Dashboard → New → Web Service
   - Connect your GitHub repository
   - Settings:
     - **Build Command:** `pip install -r requirements.txt && cd frontend && npm install && npm run build`
     - **Start Command:** `gunicorn --bind 0.0.0.0:$PORT app:app`
   - Environment Variables:
     - `DATABASE_URL`: Your MySQL connection string
     - `FLASK_ENV`: `production`

### Environment Variables

- `DATABASE_URL`: MySQL connection string from Render
- `PORT`: Set automatically by Render
- `FLASK_ENV`: Set to `production` for deployment

## API Endpoints

- `GET /api/health` - Health check
- `GET /api/tasks` - Get all tasks
- `POST /api/tasks` - Create a task
- `PUT /api/tasks/:id` - Update a task
- `DELETE /api/tasks/:id` - Delete a task

## Project Structure

```
├── app.py              # Flask backend
├── requirements.txt    # Python dependencies
├── render.yaml         # Render deployment config
├── build.sh           # Build script
├── frontend/
│   ├── package.json   # Node.js dependencies
│   ├── vite.config.js # Vite configuration
│   ├── index.html     # HTML template
│   └── src/
│       ├── main.js    # Vue.js entry point
│       └── App.vue    # Main Vue component
└── static/            # Built frontend files (generated)
```