import React, { useState } from 'react';
import { signIn } from '../lib/auth';
import { useRouter } from 'next/router';
import Link from 'next/link';

const LoginPage: React.FC = () => {
  const [formData, setFormData] = useState({ email: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // Use Better Auth's signIn function
      const result = await signIn('credentials', {
        email: formData.email,
        password: formData.password,
        redirect: false,
      });

      if (result?.error) {
        setError(result.error);
      } else {
        // Redirect to dashboard
        router.push('/dashboard');
      }
    } catch (err: any) {
      setError(err.message || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-pastel-lavender to-pastel-blue flex items-center justify-center p-4">
      <div className="w-full max-w-md bg-white bg-opacity-80 backdrop-blur-sm rounded-2xl shadow-xl p-8 border border-pastel-blue animate-fade-in">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">Welcome Back</h1>
          <p className="text-gray-600">Sign in to your account</p>
        </div>

        {error && (
          <div className="bg-pastel-pink text-red-800 p-3 rounded-lg mb-4 text-center">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="mb-5">
            <label htmlFor="email" className="block text-gray-700 mb-2">Email</label>
            <input
              id="email"
              type="email"
              value={formData.email}
              onChange={(e) => setFormData({...formData, email: e.target.value})}
              className="w-full p-3 border border-pastel-gray rounded-lg focus:outline-none focus:ring-2 focus:ring-pastel-blue focus:border-transparent"
              placeholder="your@email.com"
              required
            />
          </div>

          <div className="mb-6">
            <label htmlFor="password" className="block text-gray-700 mb-2">Password</label>
            <input
              id="password"
              type="password"
              value={formData.password}
              onChange={(e) => setFormData({...formData, password: e.target.value})}
              className="w-full p-3 border border-pastel-gray rounded-lg focus:outline-none focus:ring-2 focus:ring-pastel-blue focus:border-transparent"
              placeholder="••••••••"
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-pastel-blue hover:bg-blue-300 text-white font-medium py-3 px-4 rounded-lg transition-all duration-200 shadow-md hover:shadow-lg disabled:opacity-50"
          >
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-gray-600">
            Don't have an account?{' '}
            <Link href="/register" className="text-pastel-blue hover:underline font-medium">
              Sign up
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;