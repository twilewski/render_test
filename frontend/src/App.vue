<template>
  <div id="app">
    <header>
      <h1>Task Manager</h1>
    </header>
    
    <main>
      <div class="add-task">
        <input 
          v-model="newTask.title" 
          placeholder="Task title"
          @keyup.enter="addTask"
        />
        <input 
          v-model="newTask.description" 
          placeholder="Task description"
          @keyup.enter="addTask"
        />
        <button @click="addTask">Add Task</button>
      </div>

      <div class="tasks">
        <div v-for="task in tasks" :key="task.id" class="task" :class="{ completed: task.completed }">
          <div class="task-content">
            <h3>{{ task.title }}</h3>
            <p v-if="task.description">{{ task.description }}</p>
            <small>Created: {{ formatDate(task.created_at) }}</small>
          </div>
          <div class="task-actions">
            <button @click="toggleTask(task)">
              {{ task.completed ? 'Undo' : 'Complete' }}
            </button>
            <button @click="deleteTask(task.id)" class="delete">Delete</button>
          </div>
        </div>
      </div>

      <div v-if="loading" class="loading">Loading...</div>
      <div v-if="error" class="error">{{ error }}</div>
    </main>
  </div>
</template>

<script>
import axios from 'axios'

const API_BASE = import.meta.env.PROD ? '/api' : 'http://localhost:5000/api'

export default {
  name: 'App',
  data() {
    return {
      tasks: [],
      newTask: {
        title: '',
        description: ''
      },
      loading: false,
      error: null
    }
  },
  mounted() {
    this.fetchTasks()
  },
  methods: {
    async fetchTasks() {
      this.loading = true
      this.error = null
      try {
        const response = await axios.get(`${API_BASE}/tasks`)
        this.tasks = response.data
      } catch (error) {
        this.error = 'Failed to fetch tasks'
        console.error('Error fetching tasks:', error)
      } finally {
        this.loading = false
      }
    },
    async addTask() {
      if (!this.newTask.title.trim()) return
      
      try {
        const response = await axios.post(`${API_BASE}/tasks`, this.newTask)
        this.tasks.push(response.data)
        this.newTask.title = ''
        this.newTask.description = ''
      } catch (error) {
        this.error = 'Failed to add task'
        console.error('Error adding task:', error)
      }
    },
    async toggleTask(task) {
      try {
        const response = await axios.put(`${API_BASE}/tasks/${task.id}`, {
          ...task,
          completed: !task.completed
        })
        const index = this.tasks.findIndex(t => t.id === task.id)
        this.tasks[index] = response.data
      } catch (error) {
        this.error = 'Failed to update task'
        console.error('Error updating task:', error)
      }
    },
    async deleteTask(taskId) {
      if (!confirm('Are you sure you want to delete this task?')) return
      
      try {
        await axios.delete(`${API_BASE}/tasks/${taskId}`)
        this.tasks = this.tasks.filter(t => t.id !== taskId)
      } catch (error) {
        this.error = 'Failed to delete task'
        console.error('Error deleting task:', error)
      }
    },
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString()
    }
  }
}
</script>

<style scoped>
#app {
  max-width: 800px;
  margin: 0 auto;
}

header {
  text-align: center;
  margin-bottom: 2rem;
}

.add-task {
  display: flex;
  gap: 10px;
  margin-bottom: 2rem;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.add-task input {
  flex: 1;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.add-task button {
  padding: 10px 20px;
  background: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.add-task button:hover {
  background: #0056b3;
}

.task {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 15px;
  margin-bottom: 10px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.task.completed {
  opacity: 0.7;
}

.task.completed h3 {
  text-decoration: line-through;
}

.task-content {
  flex: 1;
}

.task-content h3 {
  margin: 0 0 5px 0;
}

.task-content p {
  margin: 0 0 10px 0;
  color: #666;
}

.task-content small {
  color: #999;
}

.task-actions {
  display: flex;
  gap: 10px;
}

.task-actions button {
  padding: 5px 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.task-actions button:first-child {
  background: #28a745;
  color: white;
}

.task-actions button.delete {
  background: #dc3545;
  color: white;
}

.loading, .error {
  text-align: center;
  padding: 20px;
}

.error {
  color: #dc3545;
  background: #f8d7da;
  border-radius: 4px;
}
</style>