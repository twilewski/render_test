from flask import Flask, request, jsonify, send_from_directory, send_file
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

app = Flask(__name__, static_folder='static')
CORS(app)

# Database configuration
database_url = os.getenv('DATABASE_URL', 'sqlite:///local.db')
if database_url.startswith('mysql://'):
    database_url = database_url.replace('mysql://', 'mysql+pymysql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'completed': self.completed,
            'created_at': self.created_at.isoformat()
        }

# API Routes
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.json
    task = Task(
        title=data.get('title'),
        description=data.get('description', '')
    )
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.json
    
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)
    
    db.session.commit()
    return jsonify(task.to_dict())

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return '', 204

# Serve frontend
@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if path.startswith('api/'):
        return jsonify({'error': 'API endpoint not found'}), 404
    try:
        return send_from_directory(app.static_folder, path)
    except:
        return send_from_directory(app.static_folder, 'index.html')

# Initialize database
@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)