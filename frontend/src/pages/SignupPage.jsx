import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../utils/store';
import { Mail, Lock, User, ArrowRight } from 'lucide-react';

export const SignupPage = () => {
  const navigate = useNavigate();
  const { signup, error } = useAuthStore();
  const [formData, setFormData] = useState({
    email: '',
    fullName: '',
    password: '',
    confirmPassword: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (formData.password !== formData.confirmPassword) {
      alert('Passwords do not match');
      return;
    }

    try {
      await signup(formData.email, formData.fullName, formData.password);
      navigate('/onboard');
    } catch (err) {
      console.error('Signup failed:', err);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0a0e27] to-[#1a1f3a] flex items-center justify-center p-4">
      <div className="glass-effect p-8 rounded-lg shadow-2xl w-full max-w-md">
        <div className="mb-8">
          <h1 className="text-3xl font-bold neon-text mb-2">InterviewPilot</h1>
          <p className="text-gray-400">Your AI-powered interview companion</p>
        </div>

        {error && (
          <div className="bg-red-500 bg-opacity-10 border border-red-500 text-red-300 p-3 rounded mb-6">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Email
            </label>
            <div className="relative">
              <Mail className="absolute left-3 top-3 text-gray-500" size={20} />
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className="w-full pl-10 pr-4 py-2 bg-[#1a1f3a] border border-gray-600 rounded focus:border-green-500 focus:outline-none text-white"
                placeholder="you@example.com"
                required
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Full Name
            </label>
            <div className="relative">
              <User className="absolute left-3 top-3 text-gray-500" size={20} />
              <input
                type="text"
                name="fullName"
                value={formData.fullName}
                onChange={handleChange}
                className="w-full pl-10 pr-4 py-2 bg-[#1a1f3a] border border-gray-600 rounded focus:border-green-500 focus:outline-none text-white"
                placeholder="John Doe"
                required
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Password
            </label>
            <div className="relative">
              <Lock className="absolute left-3 top-3 text-gray-500" size={20} />
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                className="w-full pl-10 pr-4 py-2 bg-[#1a1f3a] border border-gray-600 rounded focus:border-green-500 focus:outline-none text-white"
                placeholder="Min. 8 characters"
                required
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-300 mb-2">
              Confirm Password
            </label>
            <div className="relative">
              <Lock className="absolute left-3 top-3 text-gray-500" size={20} />
              <input
                type="password"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                className="w-full pl-10 pr-4 py-2 bg-[#1a1f3a] border border-gray-600 rounded focus:border-green-500 focus:outline-none text-white"
                placeholder="Confirm password"
                required
              />
            </div>
          </div>

          <button
            type="submit"
            className="w-full bg-gradient-to-r from-green-500 to-cyan-500 text-black font-bold py-2 rounded hover:shadow-lg hover:shadow-green-500/50 transition flex items-center justify-center gap-2"
          >
            Create Account
            <ArrowRight size={20} />
          </button>
        </form>

        <p className="mt-6 text-center text-gray-400">
          Already have an account?{' '}
          <a href="/login" className="text-green-400 hover:text-green-300">
            Login
          </a>
        </p>
      </div>
    </div>
  );
};
