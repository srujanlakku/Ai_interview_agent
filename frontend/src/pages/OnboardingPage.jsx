import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useProfileStore } from '../utils/store';
import { profileAPI } from '../services/api';
import { Briefcase, Code, Users, Clock, BarChart3 } from 'lucide-react';

export const OnboardingPage = () => {
  const navigate = useNavigate();
  const { setProfile, setLoading, setError } = useProfileStore();
  const [formData, setFormData] = useState({
    target_company: '',
    target_role: '',
    interview_type: 'Mixed',
    experience_level: 'Junior',
    available_hours: 10,
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: isNaN(value) ? value : parseFloat(value),
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const userId = 1; // TODO: Get from auth context
      const response = await profileAPI.onboard(userId, formData);
      setProfile(response.data);
      navigate('/dashboard');
    } catch (error) {
      setError('Failed to onboard. Please try again.');
      console.error('Onboarding error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0a0e27] to-[#1a1f3a] p-4">
      <div className="max-w-2xl mx-auto">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold neon-text mb-2">Let's Get Started</h1>
          <p className="text-gray-400">Tell us about your interview goals</p>
        </div>

        <div className="glass-effect p-8 rounded-lg">
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  <Briefcase className="inline mr-2" size={16} />
                  Target Company
                </label>
                <input
                  type="text"
                  name="target_company"
                  value={formData.target_company}
                  onChange={handleChange}
                  className="w-full px-4 py-2 bg-[#1a1f3a] border border-gray-600 rounded focus:border-green-500 focus:outline-none text-white"
                  placeholder="e.g., Google, Meta, Microsoft"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  <Code className="inline mr-2" size={16} />
                  Target Role
                </label>
                <input
                  type="text"
                  name="target_role"
                  value={formData.target_role}
                  onChange={handleChange}
                  className="w-full px-4 py-2 bg-[#1a1f3a] border border-gray-600 rounded focus:border-green-500 focus:outline-none text-white"
                  placeholder="e.g., Software Engineer"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  <Users className="inline mr-2" size={16} />
                  Interview Type
                </label>
                <select
                  name="interview_type"
                  value={formData.interview_type}
                  onChange={handleChange}
                  className="w-full px-4 py-2 bg-[#1a1f3a] border border-gray-600 rounded focus:border-green-500 focus:outline-none text-white"
                >
                  <option>HR</option>
                  <option>Technical</option>
                  <option>Managerial</option>
                  <option>Mixed</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  <BarChart3 className="inline mr-2" size={16} />
                  Experience Level
                </label>
                <select
                  name="experience_level"
                  value={formData.experience_level}
                  onChange={handleChange}
                  className="w-full px-4 py-2 bg-[#1a1f3a] border border-gray-600 rounded focus:border-green-500 focus:outline-none text-white"
                >
                  <option>Fresher</option>
                  <option>Junior</option>
                  <option>Mid</option>
                  <option>Senior</option>
                </select>
              </div>

              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-300 mb-2">
                  <Clock className="inline mr-2" size={16} />
                  Available Hours for Preparation
                </label>
                <input
                  type="number"
                  name="available_hours"
                  value={formData.available_hours}
                  onChange={handleChange}
                  className="w-full px-4 py-2 bg-[#1a1f3a] border border-gray-600 rounded focus:border-green-500 focus:outline-none text-white"
                  min="1"
                  max="100"
                  required
                />
              </div>
            </div>

            <button
              type="submit"
              className="w-full bg-gradient-to-r from-green-500 to-cyan-500 text-black font-bold py-3 rounded hover:shadow-lg hover:shadow-green-500/50 transition"
            >
              Start Preparation
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};
