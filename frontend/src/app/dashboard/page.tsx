'use client';

import { useState, useEffect } from 'react';
import { Todo } from '../../types/todo';
import TodoList from '../../components/TodoList';
import TodoForm from '../../components/TodoForm';
import { apiClient } from '../../lib/api';
import ProtectedRoute from '../../components/auth/ProtectedRoute';
import { useAuth } from '../../contexts/AuthContext';
import { useRouter } from 'next/navigation';

export default function DashboardPage() {
  const { user, logout } = useAuth();
  const router = useRouter();
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [showForm, setShowForm] = useState<boolean>(false);
  const [editingTodo, setEditingTodo] = useState<Todo | null>(null);
  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all');

  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    try {
      setLoading(true);
      setError(null);

      let completedFilter: boolean | undefined = undefined;
      if (filter === 'active') {
        completedFilter = false;
      } else if (filter === 'completed') {
        completedFilter = true;
      }

      const response = await apiClient.getTodos(50, 0, completedFilter);
      setTodos(response.todos);
    } catch (err) {
      if (err instanceof Error && err.message.includes('401')) {
        // If unauthorized, redirect to login
        logout();
        router.push('/login');
      } else {
        setError(err instanceof Error ? err.message : 'Failed to fetch todos');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTodo = async (todoData: any) => {
    try {
      const newTodo = await apiClient.createTodo(todoData);
      setTodos(prevTodos => [newTodo, ...(prevTodos || [])]);
      setShowForm(false);
    } catch (err) {
      if (err instanceof Error && err.message.includes('401')) {
        // If unauthorized, redirect to login
        logout();
        router.push('/login');
      } else {
        setError(err instanceof Error ? err.message : 'Failed to create todo');
      }
    }
  };

  const handleUpdateTodo = async (todoData: any) => {
    if (!editingTodo) return;

    try {
      const updatedTodo = await apiClient.updateTodo(editingTodo.id, todoData);
      setTodos(prevTodos => (prevTodos || []).map(todo => todo.id === editingTodo.id ? updatedTodo : todo));
      setEditingTodo(null);
      setShowForm(false);
    } catch (err) {
      if (err instanceof Error && err.message.includes('401')) {
        // If unauthorized, redirect to login
        logout();
        router.push('/login');
      } else {
        setError(err instanceof Error ? err.message : 'Failed to update todo');
      }
    }
  };

  const handleToggleTodo = async (id: number) => {
    const todo = todos?.find(t => t.id === id);
    if (!todo) return;

    try {
      const updatedTodo = await apiClient.partialUpdateTodo(id, { completed: !todo.completed });
      setTodos(prevTodos => (prevTodos || []).map(t => t.id === id ? updatedTodo : t));
    } catch (err) {
      if (err instanceof Error && err.message.includes('401')) {
        // If unauthorized, redirect to login
        logout();
        router.push('/login');
      } else {
        setError(err instanceof Error ? err.message : 'Failed to update todo');
      }
    }
  };

  const handleDeleteTodo = async (id: number) => {
    try {
      await apiClient.deleteTodo(id);
      setTodos(prevTodos => (prevTodos || []).filter(todo => todo.id !== id));
    } catch (err) {
      if (err instanceof Error && err.message.includes('401')) {
        // If unauthorized, redirect to login
        logout();
        router.push('/login');
      } else {
        setError(err instanceof Error ? err.message : 'Failed to delete todo');
      }
    }
  };

  const handleEditTodo = (id: number) => {
    const todo = todos?.find(t => t.id === id);
    if (todo) {
      setEditingTodo(todo);
      setShowForm(true);
    }
  };

  const [filteredTodos, setFilteredTodos] = useState<Todo[]>([]);

  useEffect(() => {
    if (todos) {
      const result = todos.filter(todo => {
        if (filter === 'active') return !todo.completed;
        if (filter === 'completed') return todo.completed;
        return true;
      });
      setFilteredTodos(result);
    } else {
      setFilteredTodos([]);
    }
  }, [todos, filter]);

  return (
    <ProtectedRoute>
      <div>
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-semibold text-gray-700">My Todos</h2>
          <div className="flex items-center space-x-4">
            <span className="text-gray-600">Welcome, {user?.username}!</span>
            <button
              onClick={() => {
                logout();
                router.push('/login');
              }}
              className="px-3 py-1 bg-red-500 text-white rounded-md hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 text-sm"
            >
              Logout
            </button>
            <button
              onClick={() => {
                setEditingTodo(null);
                setShowForm(true);
              }}
              className="px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2"
            >
              Add New Todo
            </button>
          </div>
        </div>

        <div className="mb-6 flex space-x-4">
          <button
            onClick={() => setFilter('all')}
            className={`px-3 py-1 rounded-md ${filter === 'all' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-700'}`}
          >
            All
          </button>
          <button
            onClick={() => setFilter('active')}
            className={`px-3 py-1 rounded-md ${filter === 'active' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-700'}`}
          >
            Active
          </button>
          <button
            onClick={() => setFilter('completed')}
            className={`px-3 py-1 rounded-md ${filter === 'completed' ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-700'}`}
          >
            Completed
          </button>
        </div>

        {error && (
          <div className="mb-4 p-4 bg-red-100 text-red-700 rounded-md">
            Error: {error}
          </div>
        )}

        {showForm ? (
          <div className="mb-8">
            <h3 className="text-xl font-medium text-gray-800 mb-4">
              {editingTodo ? 'Edit Todo' : 'Create New Todo'}
            </h3>
            <TodoForm
              initialData={editingTodo || undefined}
              onSubmit={editingTodo ? handleUpdateTodo : handleCreateTodo}
              onCancel={() => {
                setShowForm(false);
                setEditingTodo(null);
              }}
              isEditing={!!editingTodo}
            />
          </div>
        ) : null}

        <TodoList
          todos={filteredTodos}
          onToggle={handleToggleTodo}
          onDelete={handleDeleteTodo}
          onEdit={handleEditTodo}
          loading={loading}
          error={error || undefined}
        />
      </div>
    </ProtectedRoute>
  );
}