import React from 'react';
import { Todo } from '../types/todo';
import TodoItem from './TodoItem';

interface TodoListProps {
  todos: Todo[];
  onToggle: (id: number) => void;
  onDelete: (id: number) => void;
  onEdit: (id: number) => void;
  loading?: boolean;
  error?: string;
}

const TodoList: React.FC<TodoListProps> = ({ todos, onToggle, onDelete, onEdit, loading, error }) => {
  if (loading) {
    return (
      <div className="text-center py-8">
        <p>Loading todos...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-8">
        <p className="text-red-500">Error: {error}</p>
      </div>
    );
  }

  if (todos.length === 0) {
    return (
      <div className="text-center py-8">
        <p>No todos found. Create your first todo!</p>
      </div>
    );
  }

  return (
    <div>
      {todos.map((todo) => (
        <TodoItem
          key={todo.id}
          todo={todo}
          onToggle={onToggle}
          onDelete={onDelete}
          onEdit={onEdit}
        />
      ))}
    </div>
  );
};

export default TodoList;