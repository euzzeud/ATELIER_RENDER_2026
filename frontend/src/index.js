import React, { useEffect, useState } from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:10000';

function App() {
  const [todos, setTodos] = useState([]);
  const [newTitle, setNewTitle] = useState('');
  const [error, setError] = useState(null);

  const fetchTodos = async () => {
    try {
      const res = await fetch(`${API_URL}/todos`);
      const data = await res.json();
      setTodos(data);
    } catch (e) {
      setError('Impossible de charger les todos');
    }
  };

  useEffect(() => {
    fetchTodos();
  }, []);

  const addTodo = async () => {
    if (!newTitle.trim()) return;
    try {
      const res = await fetch(`${API_URL}/todos`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: newTitle }),
      });
      if (!res.ok) throw new Error('Create failed');
      const item = await res.json();
      setTodos((prev) => [...prev, item]);
      setNewTitle('');
    } catch (e) {
      setError('Impossible de créer le todo');
    }
  };

  const toggleDone = async (todo) => {
    try {
      const res = await fetch(`${API_URL}/todos/${todo.id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ done: !todo.done }),
      });
      if (!res.ok) throw new Error('Update failed');
      const updated = await res.json();
      setTodos((prev) => prev.map((t) => (t.id === todo.id ? updated : t)));
    } catch (e) {
      setError('Impossible de mettre à jour');
    }
  };

  const deleteTodo = async (id) => {
    try {
      const res = await fetch(`${API_URL}/todos/${id}`, { method: 'DELETE' });
      if (!res.ok) throw new Error('Delete failed');
      setTodos((prev) => prev.filter((t) => t.id !== id));
    } catch (e) {
      setError('Impossible de supprimer');
    }
  };

  return (
    <div className="app">
      <h1>Todo List React + Flask</h1>

      {error && <div className="error">{error}</div>}

      <div className="add-row">
        <input
          type="text"
          value={newTitle}
          onChange={(e) => setNewTitle(e.target.value)}
          placeholder="Ajouter une tâche"
          onKeyDown={(e) => e.key === 'Enter' && addTodo()}
        />
        <button onClick={addTodo}>Ajouter</button>
      </div>

      <ul className="todo-list">
        {todos.map((todo) => (
          <li key={todo.id} className={todo.done ? 'done' : ''}>
            <label>
              <input
                type="checkbox"
                checked={todo.done}
                onChange={() => toggleDone(todo)}
              />
              {todo.title}
            </label>
            <button className="delete" onClick={() => deleteTodo(todo.id)}>
              ×
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);