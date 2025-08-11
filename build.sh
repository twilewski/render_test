#!/bin/bash

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Creating static directory..."
mkdir -p static

echo "Checking for Node.js..."
if command -v node &> /dev/null; then
    echo "Node.js found. Building frontend..."
    cd frontend
    npm install
    npm run build
    echo "Frontend build complete!"
else
    echo "Node.js not found. Creating basic HTML fallback..."
    cat > static/index.html << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Task Manager</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        .api-test { background: #f0f0f0; padding: 15px; border-radius: 5px; margin: 20px 0; }
    </style>
</head>
<body>
    <h1>Task Manager API</h1>
    <p>The frontend build failed, but the API is working. Test the API endpoints:</p>
    <div class="api-test">
        <h3>API Endpoints:</h3>
        <ul>
            <li><a href="/api/health">GET /api/health</a> - Health check</li>
            <li><a href="/api/tasks">GET /api/tasks</a> - Get all tasks</li>
        </ul>
    </div>
    <p>Frontend will be available once Node.js build environment is properly configured.</p>
</body>
</html>
EOF
fi

echo "Build complete!"