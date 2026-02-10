import { NextRequest, NextResponse } from 'next/server';
import { headers } from 'next/headers';
import { cookies } from 'next/headers';

export async function GET(request: NextRequest, { params }: { params: { id: string } }) {
  try {
    const backendUrl = `${process.env.BACKEND_API_URL || process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'}/todos/${params.id}`;

    const response = await fetch(backendUrl, {
      headers: {
        'Authorization': headers().get('authorization') || '',
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      return NextResponse.json(
        { error: 'Failed to fetch todo' },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error fetching todo:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function PUT(request: NextRequest, { params }: { params: { id: string } }) {
  try {
    const body = await request.json();
    const backendUrl = `${process.env.BACKEND_API_URL || process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'}/todos/${params.id}`;

    const response = await fetch(backendUrl, {
      method: 'PUT',
      headers: {
        'Authorization': headers().get('authorization') || '',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      return NextResponse.json(
        { error: 'Failed to update todo' },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error updating todo:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function PATCH(request: NextRequest, { params }: { params: { id: string } }) {
  try {
    const body = await request.json();
    const backendUrl = `${process.env.BACKEND_API_URL || process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'}/todos/${params.id}`;

    const response = await fetch(backendUrl, {
      method: 'PATCH',
      headers: {
        'Authorization': headers().get('authorization') || '',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body),
    });

    if (!response.ok) {
      return NextResponse.json(
        { error: 'Failed to update todo' },
        { status: response.status }
      );
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Error partially updating todo:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}

export async function DELETE(request: NextRequest, { params }: { params: { id: string } }) {
  try {
    const backendUrl = `${process.env.BACKEND_API_URL || process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000'}/todos/${params.id}`;

    const response = await fetch(backendUrl, {
      method: 'DELETE',
      headers: {
        'Authorization': headers().get('authorization') || '',
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      return NextResponse.json(
        { error: 'Failed to delete todo' },
        { status: response.status }
      );
    }

    return new Response(null, { status: 204 });
  } catch (error) {
    console.error('Error deleting todo:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}