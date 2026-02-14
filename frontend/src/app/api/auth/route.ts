import { NextRequest, NextResponse } from 'next/server';

// Handle requests to /api/auth/* endpoints (catch-all for endpoints without specific routes)
export async function GET(request: NextRequest) {
  try {
    const url = new URL(request.url);
    // The pathname from Next.js API route already starts with /api/auth,
    // e.g., /api/auth/me
    const pathname = url.pathname;

    // Construct backend URL - ensure it includes /api/v1 prefix
    const baseUrl = process.env.BACKEND_API_URL || process.env.NEXT_PUBLIC_API_URL || process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
    // Remove trailing slash if present, then append pathname (which already includes /api/auth)
    // Replace /api/auth with /api/v1/auth to match backend API structure
    const backendPath = pathname.replace('/api/auth', '/api/v1/auth');
    const backendUrl = `${baseUrl.replace(/\/$/, '')}${backendPath}`;

    const response = await fetch(backendUrl, {
      headers: {
        'Authorization': request.headers.get('authorization') || '',
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Request failed' }));
      return NextResponse.json(errorData, { status: response.status });
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error in GET /api/auth:', error);
    return NextResponse.json(
      { detail: 'Internal server error' },
      { status: 500 }
    );
  }
}

// Handle POST requests to various auth endpoints (catch-all for endpoints without specific routes)
// Note: /api/auth/login and /api/auth/register have dedicated routes and won't hit this
export async function POST(request: NextRequest) {
  try {
    const url = new URL(request.url);
    const pathname = url.pathname; // e.g., /api/auth/some-endpoint

    // Construct backend URL - ensure it includes /api/v1 prefix
    const baseUrl = process.env.BACKEND_API_URL || process.env.NEXT_PUBLIC_API_URL || process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
    // Remove trailing slash if present, then append pathname (which already includes /api/auth)
    // Replace /api/auth with /api/v1/auth to match backend API structure
    const backendPath = pathname.replace('/api/auth', '/api/v1/auth');
    const backendUrl = `${baseUrl.replace(/\/$/, '')}${backendPath}`;

    // Try to parse body as JSON, but handle errors gracefully
    let body;
    try {
      body = await request.json();
    } catch (e) {
      // If JSON parsing fails, might be form data - return error
      return NextResponse.json(
        { detail: 'Invalid request body format' },
        { status: 400 }
      );
    }

    const response = await fetch(backendUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': request.headers.get('authorization') || '',
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Request failed' }));
      return NextResponse.json(errorData, { status: response.status });
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error in POST /api/auth:', error);
    return NextResponse.json(
      { detail: 'Internal server error' },
      { status: 500 }
    );
  }
}

// Handle PUT requests if needed
export async function PUT(request: NextRequest) {
  try {
    const url = new URL(request.url);
    const pathname = url.pathname; // e.g., /api/auth/some-endpoint
    const body = await request.json();

    // Construct backend URL - ensure it includes /api/v1 prefix
    const baseUrl = process.env.BACKEND_API_URL || process.env.NEXT_PUBLIC_API_URL || process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
    // Remove trailing slash if present, then append pathname (which already includes /api/auth)
    // Replace /api/auth with /api/v1/auth to match backend API structure
    const backendPath = pathname.replace('/api/auth', '/api/v1/auth');
    const backendUrl = `${baseUrl.replace(/\/$/, '')}${backendPath}`;

    const response = await fetch(backendUrl, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ error: 'Request failed' }));
      return NextResponse.json(errorData, { status: response.status });
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error in PUT /api/auth:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

// Handle DELETE requests if needed
export async function DELETE(request: NextRequest) {
  try {
    const url = new URL(request.url);
    const pathname = url.pathname; // e.g., /api/auth/some-endpoint

    // Construct backend URL - ensure it includes /api/v1 prefix
    const baseUrl = process.env.BACKEND_API_URL || process.env.NEXT_PUBLIC_API_URL || process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
    // Remove trailing slash if present, then append pathname (which already includes /api/auth)
    // Replace /api/auth with /api/v1/auth to match backend API structure
    const backendPath = pathname.replace('/api/auth', '/api/v1/auth');
    const backendUrl = `${baseUrl.replace(/\/$/, '')}${backendPath}`;

    const response = await fetch(backendUrl, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ error: 'Request failed' }));
      return NextResponse.json(errorData, { status: response.status });
    }

    return new Response(null, { status: 204 });
  } catch (error) {
    console.error('Error in DELETE /api/auth:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}