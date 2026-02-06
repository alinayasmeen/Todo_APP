import React from 'react';

const Footer: React.FC = () => {
  return (
    <footer className="bg-white bg-opacity-80 backdrop-blur-sm border-t border-pastel-blue py-6 mt-12">
      <div className="max-w-6xl mx-auto px-4 text-center">
        <p className="text-gray-600">
          © {new Date().getFullYear()} Todo App. Built with Next.js, Tailwind CSS, and Better Auth.
        </p>
        <div className="mt-2 flex justify-center space-x-6">
          <a href="#" className="text-pastel-blue hover:text-blue-400">Privacy Policy</a>
          <a href="#" className="text-pastel-blue hover:text-blue-400">Terms of Service</a>
          <a href="#" className="text-pastel-blue hover:text-blue-400">Contact</a>
        </div>
      </div>
    </footer>
  );
};

export default Footer;