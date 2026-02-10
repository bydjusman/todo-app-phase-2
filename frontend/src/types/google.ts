// Type definitions for Google API responses

export interface GeminiPart {
  text: string;
}

export interface GeminiContent {
  parts: GeminiPart[];
}

export interface GeminiCandidate {
  content: GeminiContent;
}

export interface GeminiResponse {
  candidates?: GeminiCandidate[];
  promptFeedback?: {
    blockReason?: string;
  };
}

export interface GeminiRequest {
  contents: {
    parts: {
      text: string;
    }[];
  }[];
}

// Response for AI-generated todo suggestions
export interface TodoSuggestion {
  title: string;
  description: string;
  priority: 'low' | 'medium' | 'high';
  suggestedDueDate?: string;
  category?: string;
}

// Response for AI-analyzed todo improvements
export interface TodoAnalysis {
  originalDescription: string;
  improvedDescription: string;
  suggestions: string[];
  estimatedTime: string;
}