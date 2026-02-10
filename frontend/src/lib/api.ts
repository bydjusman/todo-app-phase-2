import { Todo, TodoCreate, TodoUpdate, TodoListResponse } from '../types/todo';

const API_BASE_URL = process.env.NODE_ENV === 'production'
  ? '/api' // Use Next.js API routes in production
  : (process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'); // Fallback for dev

class ApiClient {
  private baseUrl: string;

  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  private getAuthToken(): string | null {
    // Get the token from localStorage
    return typeof window !== 'undefined' ? localStorage.getItem('token') : null;
  }

  private async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    const url = `${this.baseUrl}${endpoint}`;

    // Get the auth token
    const token = this.getAuthToken();

    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      if (response.status === 204) {
        // No content for DELETE requests
        return undefined as unknown as T;
      }

      return await response.json();
    } catch (error) {
      console.error(`API request failed: ${url}`, error);
      throw error;
    }
  }

  // Health check
  async healthCheck(): Promise<{ status: string; timestamp: string; version: string }> {
    return this.request('/health');
  }

  // Todo API methods
  async getTodos(limit: number = 50, offset: number = 0, completed?: boolean): Promise<TodoListResponse> {
    let url = `/todos?limit=${limit}&offset=${offset}`;
    if (completed !== undefined) {
      url += `&completed=${completed}`;
    }
    return this.request(url);
  }

  async getTodoById(id: number): Promise<Todo> {
    return this.request(`/todos/${id}`);
  }

  async createTodo(todoData: TodoCreate): Promise<Todo> {
    return this.request('/todos', {
      method: 'POST',
      body: JSON.stringify(todoData),
    });
  }

  async updateTodo(id: number, todoData: TodoUpdate): Promise<Todo> {
    return this.request(`/todos/${id}`, {
      method: 'PUT',
      body: JSON.stringify(todoData),
    });
  }

  async partialUpdateTodo(id: number, todoData: TodoUpdate): Promise<Todo> {
    return this.request(`/todos/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(todoData),
    });
  }

  async deleteTodo(id: number): Promise<void> {
    await this.request(`/todos/${id}`, {
      method: 'DELETE',
    });
  }
}

export const apiClient = new ApiClient();