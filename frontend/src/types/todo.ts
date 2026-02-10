export interface Todo {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  due_date?: string; // ISO 8601 datetime format
  created_at: string; // ISO 8601 datetime format
  updated_at: string; // ISO 8601 datetime format
}

export interface TodoCreate {
  title: string;
  description?: string;
  completed?: boolean;
  due_date?: string; // ISO 8601 datetime format
}

export interface TodoUpdate {
  title?: string;
  description?: string;
  completed?: boolean;
  due_date?: string; // ISO 8601 datetime format
}

export interface TodoListResponse {
  todos: Todo[];
  total_count: number;
  limit: number;
  offset: number;
}

export interface ApiResponse<T> {
  data?: T;
  error?: string;
  status: number;
}