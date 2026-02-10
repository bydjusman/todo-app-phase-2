'use client';

import React, { useState } from 'react';
import { googleApiService } from '../lib/googleApi';

interface TodoWithAIProps {
  onTodoGenerated?: (todo: { title: string; description: string }) => void;
}

const TodoWithAI: React.FC<TodoWithAIProps> = ({ onTodoGenerated }) => {
  const [description, setDescription] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleGenerateTitle = async () => {
    if (!description.trim()) {
      setError('Please enter a todo description');
      return;
    }

    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const title = await googleApiService.generateTodoTitle(description);
      setResult({ type: 'title', content: title });

      if (onTodoGenerated) {
        onTodoGenerated({ title, description });
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  const handleAnalyzeDescription = async () => {
    if (!description.trim()) {
      setError('Please enter a todo description');
      return;
    }

    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const analysis = await googleApiService.analyzeTodoDescription(description);
      setResult({ type: 'analysis', content: analysis });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  const handleGenerateSuggestion = async () => {
    if (!description.trim()) {
      setError('Please enter a todo description');
      return;
    }

    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      const suggestion = await googleApiService.generateTodoSuggestion(description);
      setResult({ type: 'suggestion', content: suggestion });

      if (onTodoGenerated) {
        onTodoGenerated({
          title: suggestion.title,
          description: suggestion.description
        });
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="p-4 bg-white rounded-lg shadow-md">
      <h3 className="text-lg font-semibold mb-4">AI-Powered Todo Assistance</h3>

      <div className="mb-4">
        <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
          Todo Description
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Describe your todo..."
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          rows={3}
        />
      </div>

      <div className="flex flex-wrap gap-2 mb-4">
        <button
          onClick={handleGenerateTitle}
          disabled={isLoading}
          className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Generate Title
        </button>

        <button
          onClick={handleAnalyzeDescription}
          disabled={isLoading}
          className="px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Analyze Description
        </button>

        <button
          onClick={handleGenerateSuggestion}
          disabled={isLoading}
          className="px-4 py-2 bg-purple-500 text-white rounded-md hover:bg-purple-600 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Generate Full Suggestion
        </button>
      </div>

      {isLoading && (
        <div className="text-center py-4">
          <div className="inline-block animate-spin rounded-full h-6 w-6 border-t-2 border-b-2 border-blue-500"></div>
          <p className="mt-2">Asking AI for help...</p>
        </div>
      )}

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          <strong>Error:</strong> {error}
        </div>
      )}

      {result && (
        <div className="mt-4 p-4 bg-gray-50 rounded-md">
          <h4 className="font-medium mb-2">
            {result.type === 'title' && 'Generated Title:'}
            {result.type === 'analysis' && 'Analysis Result:'}
            {result.type === 'suggestion' && 'Todo Suggestion:'}
          </h4>

          {result.type === 'title' && (
            <p className="text-lg font-semibold">{result.content}</p>
          )}

          {result.type === 'analysis' && (
            <div>
              <p><strong>Original:</strong> {result.content.originalDescription}</p>
              <p><strong>Improved:</strong> {result.content.improvedDescription}</p>
              <p><strong>Estimated Time:</strong> {result.content.estimatedTime}</p>
              <div>
                <strong>Suggestions:</strong>
                <ul className="list-disc pl-5 mt-1">
                  {result.content.suggestions.map((suggestion: string, idx: number) => (
                    <li key={idx}>{suggestion}</li>
                  ))}
                </ul>
              </div>
            </div>
          )}

          {result.type === 'suggestion' && (
            <div>
              <p><strong>Title:</strong> {result.content.title}</p>
              <p><strong>Description:</strong> {result.content.description}</p>
              <p><strong>Priority:</strong> {result.content.priority}</p>
              <p><strong>Suggested Due Date:</strong> {result.content.suggestedDueDate}</p>
              <p><strong>Category:</strong> {result.content.category}</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default TodoWithAI;