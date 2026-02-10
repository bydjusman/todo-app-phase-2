import React, { useState } from 'react';
import { TodoCreate, TodoUpdate } from '../types/todo';

interface TodoFormProps {
  initialData?: TodoCreate | TodoUpdate;
  onSubmit: (data: TodoCreate | TodoUpdate) => void;
  onCancel: () => void;
  isEditing?: boolean;
}

const TodoForm: React.FC<TodoFormProps> = ({ initialData, onSubmit, onCancel, isEditing = false }) => {
  const [title, setTitle] = useState(initialData?.title || '');
  const [description, setDescription] = useState(initialData?.description || '');
  const [dueDate, setDueDate] = useState(initialData?.due_date || '');
  const [completed, setCompleted] = useState(initialData?.completed || false);
  const [errors, setErrors] = useState<Record<string, string>>({});

  const validateForm = (): boolean => {
    const newErrors: Record<string, string> = {};

    if (!title.trim()) {
      newErrors.title = 'Title is required';
    } else if (title.length > 255) {
      newErrors.title = 'Title must be 255 characters or less';
    }

    if (description && description.length > 1000) {
      newErrors.description = 'Description must be 1000 characters or less';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!validateForm()) {
      return;
    }

    const formData: TodoCreate | TodoUpdate = {
      title: title.trim(),
      description: description.trim() || undefined,
      due_date: dueDate || undefined,
      completed,
    };

    onSubmit(formData);
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow-md">
      <div className="mb-4">
        <label htmlFor="title" className="block text-gray-700 font-medium mb-2">
          Title *
        </label>
        <input
          type="text"
          id="title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className={`w-full px-3 py-2 border rounded-md ${errors.title ? 'border-red-500' : 'border-gray-300'}`}
          placeholder="Enter todo title"
          aria-invalid={!!errors.title}
          aria-describedby={errors.title ? "title-error" : undefined}
        />
        {errors.title && (
          <p id="title-error" className="text-red-500 text-sm mt-1">
            {errors.title}
          </p>
        )}
      </div>

      <div className="mb-4">
        <label htmlFor="description" className="block text-gray-700 font-medium mb-2">
          Description
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className={`w-full px-3 py-2 border rounded-md ${errors.description ? 'border-red-500' : 'border-gray-300'}`}
          placeholder="Enter todo description (optional)"
          rows={3}
        />
        {errors.description && (
          <p className="text-red-500 text-sm mt-1">
            {errors.description}
          </p>
        )}
      </div>

      <div className="mb-4">
        <label htmlFor="dueDate" className="block text-gray-700 font-medium mb-2">
          Due Date
        </label>
        <input
          type="datetime-local"
          id="dueDate"
          value={dueDate}
          onChange={(e) => setDueDate(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md"
        />
      </div>

      <div className="mb-6 flex items-center">
        <input
          type="checkbox"
          id="completed"
          checked={completed}
          onChange={(e) => setCompleted(e.target.checked)}
          className="h-4 w-4 text-blue-600 rounded"
        />
        <label htmlFor="completed" className="ml-2 text-gray-700">
          Mark as completed
        </label>
      </div>

      <div className="flex space-x-3">
        <button
          type="submit"
          className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        >
          {isEditing ? 'Update Todo' : 'Create Todo'}
        </button>
        <button
          type="button"
          onClick={onCancel}
          className="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
        >
          Cancel
        </button>
      </div>
    </form>
  );
};

export default TodoForm;