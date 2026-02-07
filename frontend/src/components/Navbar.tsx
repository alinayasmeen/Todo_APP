import React from 'react';
import Link from 'next/link';
import { useAuth } from '../context/auth';
import { useRouter } from 'next/router';

const Navbar: React.FC = () => {
  const { user, logout } = useAuth();
  const router = useRouter();

  const handleLogout = async () => {
    await logout();
    router.push('/');
  };

  return (
    <nav className="bg-white bg-opacity-80 backdrop-blur-sm border-b border-pastel-blue py-4 px-6 shadow-sm sticky top-0 z-10">
      <div className="max-w-6xl mx-auto flex justify-between items-center">
        <Link href="/" className="text-2xl font-bold text-pastel-blue">
          Todo App
        </Link>

        <div className="flex items-center space-x-4">
          {user ? (
            <>
              <span className="text-gray-700">Hello, {user.name || user.email}</span>
              <Link
                href="/dashboard"
                className={`px-4 py-2 rounded-lg transition-colors ${
                  router.pathname === '/dashboard'
                    ? 'bg-pastel-blue text-white'
                    : 'hover:bg-pastel-blue hover:text-white'
                }`}
              >
                Dashboard
              </Link>
              <button
                onClick={handleLogout}
                className="bg-pastel-pink hover:bg-pink-300 text-white font-medium py-2 px-4 rounded-lg transition-all duration-200 shadow-md hover:shadow-lg"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link
                href="/login"
                className={`px-4 py-2 rounded-lg transition-colors ${
                  router.pathname === '/login'
                    ? 'bg-pastel-blue text-white'
                    : 'hover:bg-pastel-blue hover:text-white'
                }`}
              >
                Login
              </Link>
              <Link
                href="/register"
                className={`px-4 py-2 rounded-lg transition-colors ${
                  router.pathname === '/register'
                    ? 'bg-pastel-green text-white'
                    : 'hover:bg-pastel-green hover:text-white'
                }`}
              >
                Register
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;