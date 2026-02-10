'use client';

import React from 'react';
import Link from 'next/link';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function HomePage() {
  const router = useRouter();

  // Check if user is authenticated and redirect accordingly
  useEffect(() => {
    const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;

    if (token) {
      // If there's a token, redirect to dashboard after a brief delay
      const timer = setTimeout(() => {
        router.push('/dashboard');
      }, 1000); // 1 second delay to show welcome message

      return () => clearTimeout(timer);
    }
  }, [router]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex flex-col justify-center items-center px-4">
      <div className="max-w-4xl w-full text-center">
        <h1 className="text-4xl md:text-6xl font-bold text-gray-800 mb-6">
          Welcome to <span className="text-blue-600">Todo App</span>
        </h1>

        <p className="text-lg md:text-xl text-gray-600 mb-10 max-w-2xl mx-auto">
          Organize your life, boost your productivity. Manage your tasks efficiently with our intuitive todo application.
        </p>

        <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
          <Link
            href="/login"
            className="px-8 py-3 bg-blue-600 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 transition duration-300 transform hover:scale-105"
          >
            Login to Account
          </Link>

          <Link
            href="/login?mode=signup"
            className="px-8 py-3 bg-green-600 text-white font-semibold rounded-lg shadow-md hover:bg-green-700 transition duration-300 transform hover:scale-105"
          >
            Create New Account
          </Link>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6 max-w-2xl mx-auto">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4">Features</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-4 bg-blue-50 rounded-lg">
              <h3 className="font-medium text-blue-700">Task Management</h3>
              <p className="text-sm text-gray-600 mt-1">Create, update, and organize your tasks</p>
            </div>
            <div className="p-4 bg-green-50 rounded-lg">
              <h3 className="font-medium text-green-700">Secure Login</h3>
              <p className="text-sm text-gray-600 mt-1">Protect your data with secure authentication</p>
            </div>
            <div className="p-4 bg-purple-50 rounded-lg">
              <h3 className="font-medium text-purple-700">Responsive Design</h3>
              <p className="text-sm text-gray-600 mt-1">Access your todos anywhere, anytime</p>
            </div>
          </div>
        </div>
      </div>

      <footer className="mt-12 text-center text-gray-500 text-sm">
        <p>© {new Date().getFullYear()} Todo App - Phase II. All rights reserved.</p>
      </footer>
    </div>
  );
}