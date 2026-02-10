import React from 'react';
import type { Metadata } from 'next';
import './globals.css';
import { Providers } from './providers';

export const metadata: Metadata = {
  title: 'Todo App - Phase II',
  description: 'A full-stack todo application with Next.js and FastAPI',
  icons: {
    icon: '/favicon.ico',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-gray-100 min-h-screen">
        <Providers>
          <div className="container mx-auto px-4 py-8">
            <header className="mb-8">
              <h1 className="text-3xl font-bold text-center text-gray-800">Todo App - Phase II</h1>
              <p className="text-center text-gray-600 mt-2">A full-stack todo application</p>
            </header>
            <main>{children}</main>
            <footer className="mt-12 text-center text-gray-500 text-sm">
              <p>© {new Date().getFullYear()} Todo App - Phase II</p>
            </footer>
          </div>
        </Providers>
      </body>
    </html>
  );
}