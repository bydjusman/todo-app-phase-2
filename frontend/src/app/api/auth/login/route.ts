import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    // Check content type to handle both form-encoded and JSON
    const contentType = request.headers.get('content-type') || '';
    
    let username: string;
    let password: string;

    if (contentType.includes('application/x-www-form-urlencoded')) {
      // Handle form-encoded data
      const formData = await request.formData();
      username = formData.get('username') as string;
      password = formData.get('password') as string;
    } else {
      // Handle JSON data
      const body = await request.json();
      username = body.username;
      password = body.password;
    }

    if (!username || !password) {
      return NextResponse.json(
        { detail: 'Username and password are required' },
        { status: 400 }
      );
    }

    // Construct backend URL - ensure it includes /api/v1 prefix
    const baseUrl = process.env.BACKEND_API_URL || process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
    // Remove trailing slash if present, then add /api/v1/auth/login
    const backendUrl = `${baseUrl.replace(/\/$/, '')}/api/v1/auth/login`;

    console.log('Login request to:', backendUrl);

    // For login, FastAPI OAuth2PasswordRequestForm expects form-encoded data
    const formData = new URLSearchParams({
      username,
      password,
    });

    const response = await fetch(backendUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Login failed' }));
      console.error('Backend login error:', errorData);
      return NextResponse.json(errorData, { status: response.status });
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error in POST /api/auth/login:', error);
    return NextResponse.json(
      { detail: 'Internal server error' },
      { status: 500 }
    );
  }
}