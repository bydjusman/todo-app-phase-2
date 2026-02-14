import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();

    // Validate required fields
    if (!body.username || !body.email || !body.password) {
      return NextResponse.json(
        { detail: 'Username, email, and password are required' },
        { status: 400 }
      );
    }

    // Basic email format validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(body.email)) {
      return NextResponse.json(
        { detail: 'Invalid email format' },
        { status: 400 }
      );
    }

    // Construct backend URL - ensure it includes /api/v1 prefix
    const baseUrl = process.env.BACKEND_API_URL || process.env.NEXT_PUBLIC_API_URL || process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
    // Remove trailing slash if present, then add /api/v1/auth/register
    const backendUrl = `${baseUrl.replace(/\/$/, '')}/api/v1/auth/register`;

    // Prepare request body matching UserCreate model
    const requestBody = {
      username: body.username.trim(),
      email: body.email.trim().toLowerCase(), // Normalize email
      password: body.password,
      confirm_password: body.confirm_password || body.password, // Use confirm_password if provided, otherwise use password
    };

    console.log('Register request to:', backendUrl);
    console.log('Request body:', { ...requestBody, password: '***', confirm_password: '***' });

    const response = await fetch(backendUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Registration failed' }));
      console.error('Backend error:', errorData);
      return NextResponse.json(errorData, { status: response.status });
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error: any) {
    console.error('Error in POST /api/auth/register:', error);
    return NextResponse.json(
      { detail: error.message || 'Internal server error' },
      { status: 500 }
    );
  }
}