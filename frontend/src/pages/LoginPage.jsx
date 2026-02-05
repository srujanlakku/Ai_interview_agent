import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../utils/store';
import { Mail, Lock, ArrowRight, Briefcase, Shield, TrendingUp } from 'lucide-react';

export const LoginPage = () => {
  const navigate = useNavigate();
  const { login, error } = useAuthStore();
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await login(formData.email, formData.password);
      navigate('/dashboard');
    } catch (err) {
      console.error('Login failed:', err);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center p-4 relative overflow-hidden bg-black">
      <div className="cyber-panel p-8 rounded-lg w-full max-w-md relative z-10">
        <div className="mb-8 text-center">
          <div className="flex justify-center mb-4">
            <div className="bg-red-600 p-3 rounded-full glow-border">
              <Briefcase className="text-white" size={24} />
            </div>
          </div>
          <h1 className="text-3xl font-bold cyber-section-title mb-2">NEXUS INTERVIEW</h1>
          <p className="text-white text-sm uppercase tracking-widest opacity-80">SYSTEM ACCESS PROTOCOL</p>
        </div>

        {error && (
          <div className="cyber-alert cyber-alert-danger mb-6 flex items-center gap-2">
            <Shield size={16} />
            <span className="font-mono">{error}</span>
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-5">
          <div>
            <label className="block text-sm font-mono text-white mb-2 flex items-center gap-2 uppercase tracking-wider">
              <Mail size={16} className="text-red-500" />
              USER IDENTIFICATION
            </label>
            <div className="relative">
              <Mail className="absolute left-3 top-3.5 text-red-500" size={18} />
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleChange}
                className="w-full pl-10 pr-4 py-3 bg-black border border-red-500 rounded-none focus:border-red-400 focus:outline-none text-white font-mono transition-all glow-border"
                placeholder="ENTER IDENTIFICATION CODE"
                required
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-mono text-white mb-2 flex items-center gap-2 uppercase tracking-wider">
              <Lock size={16} className="text-red-500" />
              AUTHENTICATION KEY
            </label>
            <div className="relative">
              <Lock className="absolute left-3 top-3.5 text-red-500" size={18} />
              <input
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                className="w-full pl-10 pr-4 py-3 bg-black border border-red-500 rounded-none focus:border-red-400 focus:outline-none text-white font-mono transition-all glow-border"
                placeholder="••••••••"
                required
              />
            </div>
          </div>

          <button
            type="submit"
            className="w-full cyber-btn cyber-btn-primary flex items-center justify-center gap-2 py-3 mt-2 font-mono uppercase tracking-wider"
          >
            <span>INITIATE SYSTEM ACCESS</span>
            <ArrowRight size={18} />
          </button>
        </form>

        <div className="mt-8 pt-6 border-t border-red-500">
          <p className="text-center text-white text-sm mb-4 font-mono uppercase tracking-widest opacity-70">
            &#62;&#62; NEW USER DETECTED &#60;&#60;
          </p>
          <a 
            href="/signup" 
            className="cyber-btn cyber-btn-secondary w-full flex items-center justify-center gap-2 py-3 font-mono uppercase tracking-wider"
          >
            <TrendingUp size={18} />
            <span>REGISTER FOR ACCESS</span>
          </a>
        </div>
        
        {/* System Status */}
        <div className="mt-6 grid grid-cols-3 gap-3 text-center">
          <div className="cyber-badge cyber-badge-success text-xs">
            <Shield className="mx-auto mb-1" size={16} />
            SECURE
          </div>
          <div className="cyber-badge text-xs">
            <TrendingUp className="mx-auto mb-1" size={16} />
            ACTIVE
          </div>
          <div className="cyber-badge cyber-badge-info text-xs">
            <Briefcase className="mx-auto mb-1" size={16} />
            ONLINE
          </div>
        </div>
      </div>
    </div>
  );
};