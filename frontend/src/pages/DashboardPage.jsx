import React, { useEffect, useState } from 'react';
import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { interviewAPI } from '../services/api';
import { TrendingUp, Award, Target, BookOpen } from 'lucide-react';

export const DashboardPage = () => {
  const userId = 1; // TODO: Get from auth context
  const [stats, setStats] = useState(null);
  const [interviews, setInterviews] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [statsRes, interviewsRes] = await Promise.all([
          interviewAPI.getStatistics(userId),
          interviewAPI.getUserInterviews(userId),
        ]);
        setStats(statsRes.data);
        setInterviews(interviewsRes.data);
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-[#0a0e27] to-[#1a1f3a] flex items-center justify-center">
        <div className="text-gray-400">Loading dashboard...</div>
      </div>
    );
  }

  const scoreData = interviews.map((interview, idx) => ({
    name: `Interview ${idx + 1}`,
    score: interview.score || 0,
  }));

  const readinessConfig = {
    'Not Ready': 0,
    'Almost Ready': 1,
    'Interview Ready': 2,
  };

  const readinessData = [
    { name: 'Progress', value: readinessConfig[stats?.readiness_level || 'Not Ready'] || 0 },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0a0e27] to-[#1a1f3a] p-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold neon-text mb-2">Dashboard</h1>
          <p className="text-gray-400">Your interview preparation progress</p>
        </div>

        {/* Stats Cards */}
        <div className="grid md:grid-cols-4 gap-4 mb-8">
          <div className="glass-effect p-6 rounded-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Average Score</p>
                <p className="text-2xl font-bold text-green-400">{stats?.average_score?.toFixed(1)}/10</p>
              </div>
              <Award className="text-green-500" size={40} />
            </div>
          </div>

          <div className="glass-effect p-6 rounded-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Total Interviews</p>
                <p className="text-2xl font-bold text-cyan-400">{stats?.total_interviews}</p>
              </div>
              <Target className="text-cyan-500" size={40} />
            </div>
          </div>

          <div className="glass-effect p-6 rounded-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Highest Score</p>
                <p className="text-2xl font-bold text-yellow-400">{stats?.highest_score}/10</p>
              </div>
              <TrendingUp className="text-yellow-500" size={40} />
            </div>
          </div>

          <div className="glass-effect p-6 rounded-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-400 text-sm">Readiness</p>
                <p className="text-xl font-bold text-purple-400">{stats?.readiness_level}</p>
              </div>
              <BookOpen className="text-purple-500" size={40} />
            </div>
          </div>
        </div>

        {/* Charts */}
        <div className="grid md:grid-cols-2 gap-6 mb-8">
          <div className="glass-effect p-6 rounded-lg">
            <h2 className="text-xl font-bold text-white mb-4">Score Progress</h2>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={scoreData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#444" />
                <XAxis stroke="#888" />
                <YAxis stroke="#888" />
                <Tooltip contentStyle={{ backgroundColor: '#1a1f3a', border: '1px solid #444' }} />
                <Line type="monotone" dataKey="score" stroke="#00ff88" strokeWidth={2} dot={{ fill: '#00ff88' }} />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div className="glass-effect p-6 rounded-lg">
            <h2 className="text-xl font-bold text-white mb-4">Recent Interviews</h2>
            <div className="space-y-3">
              {interviews.slice(0, 5).map((interview) => (
                <div key={interview.id} className="flex justify-between items-center p-3 bg-[#1a1f3a] rounded">
                  <div>
                    <p className="font-medium text-white">{interview.interview_type}</p>
                    <p className="text-sm text-gray-400">{new Date(interview.created_at).toLocaleDateString()}</p>
                  </div>
                  <div className="text-right">
                    <p className="font-bold text-green-400">{interview.score?.toFixed(1)}/10</p>
                    <p className="text-xs text-gray-400">{interview.readiness_level}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex gap-4">
          <button className="flex-1 bg-gradient-to-r from-green-500 to-cyan-500 text-black font-bold py-3 rounded hover:shadow-lg hover:shadow-green-500/50 transition">
            Start New Interview
          </button>
          <button className="flex-1 bg-gradient-to-r from-purple-500 to-pink-500 text-white font-bold py-3 rounded hover:shadow-lg hover:shadow-purple-500/50 transition">
            View Study Materials
          </button>
        </div>
      </div>
    </div>
  );
};
