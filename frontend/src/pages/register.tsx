import React, { useState } from 'react';
import { signIn } from '../lib/auth';
import { useRouter } from 'next/router';
import Link from 'next/link';

const RegisterPage: React.FC = () => {
  const [formData, setFormData] = useState({ name: '', email: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      // For registration, we'll make a direct API call to the backend
      const response = await fetch(process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api' + '/auth/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: formData.name,
          email: formData.email,
          password: formData.password,
        }),
      });

      if (response.ok) {
        // Now try to sign in with the credentials
        const loginResult = await signIn('credentials', {
          email: formData.email,
          password: formData.password,
          redirect: false,
        });

        if (loginResult?.error) {
          setError(loginResult.error);
        } else {
          // Redirect to dashboard
          router.push('/dashboard');
        }
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Registration failed');
      }
    } catch (err: any) {
      setError(err.message || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-pastel-lavender to-pastel-green flex items-center justify-center p-4">
      <div className="w-full max-w-md bg-white bg-opacity-80 backdrop-blur-sm rounded-2xl shadow-xl p-8 border border-pastel-green animate-fade-in">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">Create Account</h1>
          <p className="text-gray-600">Join us today and start managing your tasks</p>
        </div>

        {error && (
          <div className="bg-pastel-pink text-red-800 p-3 rounded-lg mb-4 text-center">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="mb-5">
            <label htmlFor="name" className="block text-gray-700 mb-2">Full Name</label>
            <input
              id="name"
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({...formData, name: e.target.value})}
              className="w-full p-3 border border-pastel-gray rounded-lg focus:outline-none focus:ring-2 focus:ring-pastel-blue focus:border-transparent"
              placeholder="John Doe"
              required
            />
          </div>

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
              minLength={6}
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-pastel-green hover:bg-green-300 text-white font-medium py-3 px-4 rounded-lg transition-all duration-200 shadow-md hover:shadow-lg disabled:opacity-50"
          >
            {loading ? 'Creating account...' : 'Sign Up'}
          </button>
        </form>

        <div className="mt-6 text-center">
          <p className="text-gray-600">
            Already have an account?{' '}
            <Link href="/login" className="text-pastel-green hover:underline font-medium">
              Sign in
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;