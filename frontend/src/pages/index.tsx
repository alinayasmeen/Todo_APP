/**
 * Home Page
 *
 * This is the main landing page for the Todo App.
 * It provides navigation to login/register for unauthenticated users
 * and to the dashboard for authenticated users.
 */
import React from 'react';
import Link from 'next/link';

const HomePage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-pastel-lavender to-pastel-blue">
      <div className="max-w-6xl mx-auto px-4 py-8">
        <header className="text-center mb-12 mt-8 animate-fade-in">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-800 mb-4 bg-clip-text text-transparent bg-gradient-to-r from-pastel-blue to-pastel-purple">
            Welcome to Todo App
          </h1>
          <p className="text-xl text-gray-700 max-w-2xl mx-auto">
            Your personal task management solution with AI-powered insights
          </p>
        </header>

        <section className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
          <div className="bg-white bg-opacity-70 backdrop-blur-sm p-6 rounded-xl shadow-md border border-pastel-blue transition-transform duration-300 hover:scale-105 animate-slide-up">
            <div className="text-pastel-blue text-3xl mb-4">✓</div>
            <h2 className="text-xl font-semibold text-gray-800 mb-2">Manage Tasks</h2>
            <p className="text-gray-600">Create, update, and track your tasks efficiently</p>
          </div>

          <div className="bg-white bg-opacity-70 backdrop-blur-sm p-6 rounded-xl shadow-md border border-pastel-green transition-transform duration-300 hover:scale-105 animate-slide-up delay-100">
            <div className="text-pastel-green text-3xl mb-4">🔒</div>
            <h2 className="text-xl font-semibold text-gray-800 mb-2">Secure Authentication</h2>
            <p className="text-gray-600">Protect your data with industry-standard security</p>
          </div>

          <div className="bg-white bg-opacity-70 backdrop-blur-sm p-6 rounded-xl shadow-md border border-pastel-pink transition-transform duration-300 hover:scale-105 animate-slide-up delay-200">
            <div className="text-pastel-pink text-3xl mb-4">🤖</div>
            <h2 className="text-xl font-semibold text-gray-800 mb-2">AI Insights</h2>
            <p className="text-gray-600">Get smart suggestions and productivity insights</p>
          </div>
        </section>

        <section className="text-center py-8">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">Get Started Today</h2>

          <div className="flex flex-col sm:flex-row justify-center gap-4">
            <Link href="/login">
              <button className="bg-pastel-blue hover:bg-blue-300 text-white font-medium py-3 px-6 rounded-lg transition-all duration-200 shadow-md hover:shadow-lg transform hover:-translate-y-0.5">
                Login to Account
              </button>
            </Link>

            <Link href="/register">
              <button className="bg-pastel-green hover:bg-green-300 text-white font-medium py-3 px-6 rounded-lg transition-all duration-200 shadow-md hover:shadow-lg transform hover:-translate-y-0.5">
                Create Account
              </button>
            </Link>
          </div>
        </section>
      </div>
    </div>
  );
};

export default HomePage;