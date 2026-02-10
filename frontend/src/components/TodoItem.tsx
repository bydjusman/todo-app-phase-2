import React from 'react';
import { Todo } from '../types/todo';

interface TodoItemProps {
  todo: Todo;
  onToggle: (id: number) => void;
  onDelete: (id: number) => void;
  onEdit: (id: number) => void;
}

const TodoItem: React.FC<TodoItemProps> = ({ todo, onToggle, onDelete, onEdit }) => {
  return (
    <div className={`p-4 mb-2 rounded-lg border ${todo.completed ? 'bg-green-50' : 'bg-white'}`}>
      <div className="flex items-center justify-between">
        <div className="flex items-center">
          <input
            type="checkbox"
            checked={todo.completed}
            onChange={() => onToggle(todo.id)}
            className="mr-3 h-5 w-5"
            aria-label={`Mark todo "${todo.title}" as ${todo.completed ? 'incomplete' : 'complete'}`}
          />
          <div>
            <h3 className={`text-lg ${todo.completed ? 'line-through text-gray-500' : 'text-gray-800'}`}>
              {todo.title}
            </h3>
            {todo.description && (
              <p className={`mt-1 ${todo.completed ? 'line-through text-gray-500' : 'text-gray-600'}`}>
                {todo.description}
              </p>
            )}
            {todo.due_date && (
              <p className="text-sm text-gray-500 mt-1">
                Due: {new Date(todo.due_date).toLocaleDateString()}
              </p>
            )}
            <p className="text-xs text-gray-400 mt-1">
              Created: {new Date(todo.created_at).toLocaleString()}
            </p>
          </div>
        </div>
        <div className="flex space-x-2">
          <button
            onClick={() => onEdit(todo.id)}
            className="px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 text-sm"
            aria-label={`Edit todo "${todo.title}"`}
          >
            Edit
          </button>
          <button
            onClick={() => onDelete(todo.id)}
            className="px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600 text-sm"
            aria-label={`Delete todo "${todo.title}"`}
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  );
};

export default TodoItem;