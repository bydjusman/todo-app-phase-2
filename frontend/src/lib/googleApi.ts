import { Todo } from '../types/todo';
import { GeminiRequest, GeminiResponse, TodoSuggestion, TodoAnalysis } from '../types/google';

const GOOGLE_API_KEY = process.env.NEXT_PUBLIC_GOOGLE_API_KEY;

class GoogleApiService {
  private apiKey: string | undefined;

  constructor() {
    this.apiKey = GOOGLE_API_KEY;
  }

  private async request<T>(endpoint: string, data: any): Promise<T> {
    if (!this.apiKey) {
      throw new Error('Google API key is not configured');
    }

    const url = `${endpoint}?key=${this.apiKey}`;

    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error?.message || `HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error(`Google API request failed: ${url}`, error);
      throw error;
    }
  }

  // Method to interact with Gemini API
  async generateText(prompt: string): Promise<string> {
    const endpoint = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent';

    const requestData: GeminiRequest = {
      contents: [{
        parts: [{
          text: prompt
        }]
      }]
    };

    try {
      const response: GeminiResponse = await this.request(endpoint, requestData);

      if (response.candidates && response.candidates.length > 0) {
        return response.candidates[0].content.parts[0].text;
      } else {
        throw new Error('No response generated from Gemini API');
      }
    } catch (error) {
      console.error('Error generating text with Gemini:', error);
      throw error;
    }
  }

  // Method to analyze todo description using AI
  async analyzeTodoDescription(description: string): Promise<TodoAnalysis> {
    const prompt = `Analyze this todo description and provide an improved version with suggestions. Respond in JSON format with these fields: {originalDescription: "${description}", improvedDescription: "...", suggestions: [...], estimatedTime: "..."}.`;

    try {
      const response = await this.generateText(prompt);
      // Attempt to parse the response as JSON
      const parsedResponse = JSON.parse(response);
      return parsedResponse as TodoAnalysis;
    } catch (error) {
      // If parsing fails, return a basic analysis
      return {
        originalDescription: description,
        improvedDescription: description,
        suggestions: [`Consider adding more details to: ${description}`],
        estimatedTime: 'Not specified'
      };
    }
  }

  // Method to generate a todo title based on description
  async generateTodoTitle(description: string): Promise<string> {
    const prompt = `Generate a concise and effective title for this todo: "${description}". Respond with only the title.`;
    return this.generateText(prompt);
  }

  // Method to suggest due dates for a todo
  async suggestDueDate(description: string): Promise<string> {
    const prompt = `Based on this todo description, suggest an appropriate timeframe: "${description}". Respond with only the suggested timeframe (e.g., 'today', 'this week', 'this month').`;
    return this.generateText(prompt);
  }

  // Method to generate a complete todo suggestion
  async generateTodoSuggestion(description: string): Promise<TodoSuggestion> {
    const prompt = `Generate a complete todo suggestion based on this: "${description}". Respond in JSON format with these fields: {title: "...", description: "...", priority: "low|medium|high", suggestedDueDate: "...", category: "..."}.`;

    try {
      const response = await this.generateText(prompt);
      // Attempt to parse the response as JSON
      const parsedResponse = JSON.parse(response);
      return parsedResponse as TodoSuggestion;
    } catch (error) {
      // If parsing fails, return a basic suggestion
      return {
        title: description,
        description: description,
        priority: 'medium',
        suggestedDueDate: 'Not specified',
        category: 'General'
      };
    }
  }
}

export const googleApiService = new GoogleApiService();