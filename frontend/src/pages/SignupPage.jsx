import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../utils/store';
import { Mail, Lock, User, ArrowRight, Briefcase, Shield, TrendingUp } from 'lucide-react';

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
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 flex items-center justify-center p-4 relative overflow-hidden">
      {/* Background elements */}
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_10%_20%,rgba(59,130,246,0.1)_0%,transparent_20%)]"></div>
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_90%_80%,rgba(16,185,129,0.1)_0%,transparent_20%)]"></div>
      
      <div className="glass-panel p-8 rounded-xl shadow-2xl w-full max-w-md relative z-10">
        <div className="mb-8 text-center">
          <div className="flex justify-center mb-4">
            <div className="bg-blue-500 p-3 rounded-full">
              <Briefcase className="text-white" size={24} />
            </div>
          </div>
          <h1 className="text-3xl font-bold text-blue-400 mb-2">CareerPilot</h1>
          <p className="text-slate-400">Start Your Professional Journey</p>
        </div>

        {error && (
          <div className="alert alert-danger mb-6 flex items-center gap-2">
            <Shield size={16} />
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2 flex items-center gap-2">
              <Mail size={16} />
              Work Email
            </label>
            <div className="relative">
              <Mail className="absolute left-3 top-3.5 text-slate-500" size={18} />
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className="w-full pl-10 pr-4 py-3 bg-slate-800 border border-slate-700 rounded-lg focus:border-blue-500 focus:outline-none text-white transition-colors"
                placeholder="your.email@company.com"
                required
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2 flex items-center gap-2">
              <User size={16} />
              Full Name
            </label>
            <div className="relative">
              <User className="absolute left-3 top-3.5 text-slate-500" size={18} />
              <input
                type="text"
                name="fullName"
                value={formData.fullName}
                onChange={handleChange}
                className="w-full pl-10 pr-4 py-3 bg-slate-800 border border-slate-700 rounded-lg focus:border-blue-500 focus:outline-none text-white transition-colors"
                placeholder="John Smith"
                required
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2 flex items-center gap-2">
              <Lock size={16} />
              Secure Password
            </label>
            <div className="relative">
              <Lock className="absolute left-3 top-3.5 text-slate-500" size={18} />
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                className="w-full pl-10 pr-4 py-3 bg-slate-800 border border-slate-700 rounded-lg focus:border-blue-500 focus:outline-none text-white transition-colors"
                placeholder="Minimum 8 characters"
                required
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-300 mb-2 flex items-center gap-2">
              <Lock size={16} />
              Confirm Password
            </label>
            <div className="relative">
              <Lock className="absolute left-3 top-3.5 text-slate-500" size={18} />
              <input
                type="password"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                className="w-full pl-10 pr-4 py-3 bg-slate-800 border border-slate-700 rounded-lg focus:border-blue-500 focus:outline-none text-white transition-colors"
                placeholder="Confirm your password"
                required
              />
            </div>
          </div>

          <button
            type="submit"
            className="w-full btn-primary flex items-center justify-center gap-2 py-3 mt-2"
          >
            <span>Create Professional Account</span>
            <ArrowRight size={18} />
          </button>
        </form>

        <div className="mt-8 pt-6 border-t border-slate-700">
          <p className="text-center text-slate-400 text-sm mb-4">
            Already have an account?
          </p>
          <a 
            href="/login" 
            className="btn-secondary w-full flex items-center justify-center gap-2 py-3"
          >
            <Shield size={18} />
            <span>Sign In to CareerPilot</span>
          </a>
        </div>
        
        {/* Features preview */}
        <div className="mt-6 grid grid-cols-3 gap-3 text-center">
          <div className="text-xs text-slate-500">
            <Shield className="mx-auto mb-1" size={16} />
            Enterprise Security
          </div>
          <div className="text-xs text-slate-500">
            <TrendingUp className="mx-auto mb-1" size={16} />
            Career Growth
          </div>
          <div className="text-xs text-slate-500">
            <Briefcase className="mx-auto mb-1" size={16} />
            Professional Network
          </div>
        </div>
      </div>
    </div>
  );
};