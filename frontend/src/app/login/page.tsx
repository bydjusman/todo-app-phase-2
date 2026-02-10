'use client';

import React, { useState, useEffect } from 'react';
import LoginForm from '@/components/auth/LoginForm';
import SignupForm from '@/components/auth/SignupForm';
import Link from 'next/link';
import { useSearchParams } from 'next/navigation';

const LoginPage = () => {
  const searchParams = useSearchParams();
  const [showLogin, setShowLogin] = useState(true);

  useEffect(() => {
    // Check URL parameter to determine which form to show
    const mode = searchParams?.get('mode');
    if (mode === 'signup') {
      setShowLogin(false); // Show signup form by default
    } else {
      setShowLogin(true); // Show login form by default
    }
  }, [searchParams]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Todo App - Phase II
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            {showLogin ? 'Sign in to your account' : 'Create a new account'}
          </p>
        </div>

        {showLogin ? (
          <LoginForm onSwitchToSignup={() => setShowLogin(false)} />
        ) : (
          <SignupForm onSwitchToLogin={() => setShowLogin(true)} />
        )}

        <div className="text-center mt-4">
          <Link href="/" className="text-sm text-blue-600 hover:text-blue-500">
            Back to Home
          </Link>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;