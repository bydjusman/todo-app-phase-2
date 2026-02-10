# Google API Integration Guide

This document explains how the Google API (specifically Gemini) has been integrated into the frontend application.

## Files Created

1. `src/lib/googleApi.ts` - Main service for interacting with Google APIs
2. `src/types/google.ts` - Type definitions for Google API responses
3. `src/components/TodoWithAI.tsx` - Sample component demonstrating AI functionality
4. `src/components/TodoFormWithAI.tsx` - Enhanced TodoForm with AI integration

## Environment Configuration

The Google API key has been added to the `.env.local` file:

```env
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000/api
NEXT_PUBLIC_GOOGLE_API_KEY=AIzaSyAo_xW6nNWJQCx8qOy3pfcHZrXh80t2Yco
```

## Available Methods

The `googleApiService` provides the following methods:

### 1. generateText(prompt: string): Promise<string>
Direct interaction with the Gemini API to generate text based on a prompt.

### 2. generateTodoTitle(description: string): Promise<string>
Generates a concise title for a todo based on its description.

### 3. analyzeTodoDescription(description: string): Promise<TodoAnalysis>
Analyzes a todo description and provides improvement suggestions.

### 4. suggestDueDate(description: string): Promise<string>
Suggests an appropriate timeframe for completing a todo.

### 5. generateTodoSuggestion(description: string): Promise<TodoSuggestion>
Generates a complete todo suggestion with title, description, priority, and other details.

## Usage Examples

### Basic Usage
```typescript
import { googleApiService } from '../lib/googleApi';

// Generate a title for a todo
const title = await googleApiService.generateTodoTitle("Need to prepare presentation for meeting");

// Analyze a todo description
const analysis = await googleApiService.analyzeTodoDescription("Fix the login bug");
```

### Integration with Components
See `TodoWithAI.tsx` for a complete example of how to integrate AI functionality into your components.

## Type Definitions

The integration includes TypeScript interfaces for type safety:

- `GeminiRequest` - Structure for requests to the Gemini API
- `GeminiResponse` - Structure for responses from the Gemini API
- `TodoSuggestion` - Structure for AI-generated todo suggestions
- `TodoAnalysis` - Structure for AI-generated todo analysis

## Security Considerations

- The Google API key is stored in environment variables as `NEXT_PUBLIC_GOOGLE_API_KEY`
- Note that this is a public environment variable, which means it will be accessible in the browser
- For production use, consider implementing server-side proxy to protect your API key
- Monitor your API usage to prevent unauthorized access

## Error Handling

All API methods include proper error handling:
- Network errors are caught and re-thrown with descriptive messages
- Invalid responses from the API are handled gracefully
- Fallback responses are provided when JSON parsing fails

## Testing the Integration

To test the integration:

1. Ensure your Google API key is correctly set in `.env.local`
2. Run the development server: `npm run dev`
3. Access any page that uses the AI functionality
4. Monitor the browser console for any error messages

## Troubleshooting

Common issues and solutions:

1. **API Key Not Working**: Verify the key in `.env.local` is correct and has the proper permissions
2. **CORS Errors**: Ensure your Google Cloud project has the Generative Language API enabled
3. **Rate Limiting**: Check your Google Cloud billing and quota settings
4. **Invalid JSON Responses**: The service includes fallbacks, but check the API response format