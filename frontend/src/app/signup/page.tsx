'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';

export default function SignupPage() {
  const router = useRouter();

  useEffect(() => {
    // Redirect to login page with signup parameter to show signup form by default
    router.push('/login?mode=signup');
  }, [router]);

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="text-xl">Redirecting to signup...</div>
    </div>
  );
}