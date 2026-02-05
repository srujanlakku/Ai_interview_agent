import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../utils/store';
import { 
  BarChart3, 
  Brain, 
  Target, 
  Clock, 
  Trophy, 
  Users, 
  BookOpen, 
  TrendingUp,
  Shield,
  Zap,
  Compass,
  CheckCircle,
  AlertTriangle,
  Info,
  ChevronRight,
  Play,
  Pause,
  RotateCcw
} from 'lucide-react';

export const DashboardPage = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuthStore();
  const [activeTab, setActiveTab] = useState('overview');
  const [interviewStatus, setInterviewStatus] = useState('ready'); // ready, in-progress, completed

  // Mock data for demonstration
  const mockData = {
    readinessScore: 72,
    confidenceLevel: 68,
    communicationScore: 75,
    lastInterview: {
      date: '2024-01-15',
      score: 6.8,
      feedback: 'Good technical understanding but needs work on structuring responses'
    },
    upcomingRoadmap: [
      { topic: 'System Design Fundamentals', progress: 65, priority: 'high' },
      { topic: 'Behavioral Interview Prep', progress: 30, priority: 'medium' },
      { topic: 'Coding Interview Patterns', progress: 80, priority: 'high' }
    ],
    recentAnalysis: {
      primaryIssue: 'Conceptual Gap in Distributed Systems',
      confidenceTrend: 'improving',
      communicationStrengths: ['Clear explanations', 'Good technical vocabulary'],
      improvementAreas: ['Need more structured responses', 'Reduce filler words']
    }
  };

  const handleStartInterview = () => {
    setInterviewStatus('in-progress');
    // In real implementation, this would start the interview flow
    navigate('/interview');
  };

  const renderOverviewTab = () => (
    <div className="space-y-6">
      {/* Readiness Score Card */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="metric-card">
          <div className="flex items-center justify-between mb-2">
            <span className="metric-label">Readiness Score</span>
            <Trophy className="text-yellow-500" size={20} />
          </div>
          <div className="metric-value text-yellow-500">{mockData.readinessScore}%</div>
          <div className="w-full bg-slate-700 rounded-full h-2 mt-2">
            <div 
              className="bg-gradient-to-r from-yellow-500 to-orange-500 h-2 rounded-full" 
              style={{ width: `${mockData.readinessScore}%` }}
            ></div>
          </div>
          <p className="text-sm text-slate-400 mt-2">
            {mockData.readinessScore >= 80 ? 'Ready for interviews!' : 
             mockData.readinessScore >= 60 ? 'Almost ready - keep practicing' : 
             'Needs more preparation'}
          </p>
        </div>

        <div className="metric-card">
          <div className="flex items-center justify-between mb-2">
            <span className="metric-label">Confidence Level</span>
            <Zap className="text-blue-500" size={20} />
          </div>
          <div className="metric-value text-blue-500">{mockData.confidenceLevel}%</div>
          <div className="w-full bg-slate-700 rounded-full h-2 mt-2">
            <div 
              className="bg-gradient-to-r from-blue-500 to-cyan-500 h-2 rounded-full" 
              style={{ width: `${mockData.confidenceLevel}%` }}
            ></div>
          </div>
          <p className="text-sm text-slate-400 mt-2">
            {mockData.confidenceLevel >= 70 ? 'Strong confidence' : 'Room for improvement'}
          </p>
        </div>

        <div className="metric-card">
          <div className="flex items-center justify-between mb-2">
            <span className="metric-label">Communication</span>
            <Users className="text-green-500" size={20} />
          </div>
          <div className="metric-value text-green-500">{mockData.communicationScore}%</div>
          <div className="w-full bg-slate-700 rounded-full h-2 mt-2">
            <div 
              className="bg-gradient-to-r from-green-500 to-emerald-500 h-2 rounded-full" 
              style={{ width: `${mockData.communicationScore}%` }}
            ></div>
          </div>
          <p className="text-sm text-slate-400 mt-2">
            {mockData.communicationScore >= 80 ? 'Excellent communication' : 'Good communication'}
          </p>
        </div>
      </div>

      {/* Interview Actions */}
      <div className="section-card">
        <div className="section-header">
          <h2 className="section-title">
            <Play className="text-blue-500" size={20} />
            Start Your Interview Journey
          </h2>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <button 
            onClick={handleStartInterview}
            className="btn-primary flex items-center justify-center gap-2 py-4"
          >
            <Play size={20} />
            Begin Practice Interview
          </button>
          
          <button className="btn-secondary flex items-center justify-center gap-2 py-4">
            <Compass size={20} />
            View Role Roadmap
          </button>
        </div>
      </div>

      {/* Recent Analysis */}
      <div className="section-card">
        <div className="section-header">
          <h2 className="section-title">
            <Brain className="text-purple-500" size={20} />
            Latest Performance Analysis
          </h2>
        </div>
        
        <div className="space-y-4">
          <div className="alert alert-warning flex items-start gap-3">
            <AlertTriangle size={20} className="mt-0.5 flex-shrink-0" />
            <div>
              <h3 className="font-semibold text-yellow-600">Primary Improvement Area</h3>
              <p className="text-yellow-700">{mockData.recentAnalysis.primaryIssue}</p>
            </div>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <h4 className="font-medium text-slate-300 mb-2">Strengths Identified</h4>
              <ul className="space-y-1">
                {mockData.recentAnalysis.communicationStrengths.map((strength, index) => (
                  <li key={index} className="flex items-center gap-2 text-sm">
                    <CheckCircle size={16} className="text-green-500" />
                    <span className="text-slate-400">{strength}</span>
                  </li>
                ))}
              </ul>
            </div>
            
            <div>
              <h4 className="font-medium text-slate-300 mb-2">Focus Areas</h4>
              <ul className="space-y-1">
                {mockData.recentAnalysis.improvementAreas.map((area, index) => (
                  <li key={index} className="flex items-center gap-2 text-sm">
                    <Info size={16} className="text-blue-500" />
                    <span className="text-slate-400">{area}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderRoadmapTab = () => (
    <div className="space-y-6">
      <div className="section-card">
        <div className="section-header">
          <h2 className="section-title">
            <Compass className="text-purple-500" size={20} />
            Your Personalized Career Roadmap
          </h2>
          <span className="badge badge-info">Software Engineer Path</span>
        </div>
        
        <div className="space-y-4">
          {mockData.upcomingRoadmap.map((item, index) => (
            <div key={index} className="glass-card p-4">
              <div className="flex items-center justify-between mb-2">
                <h3 className="font-medium text-slate-200">{item.topic}</h3>
                <span className={`badge ${
                  item.priority === 'high' ? 'badge-danger' : 
                  item.priority === 'medium' ? 'badge-warning' : 'badge-info'
                }`}>
                  {item.priority} priority
                </span>
              </div>
              <div className="w-full bg-slate-700 rounded-full h-2">
                <div 
                  className={`h-2 rounded-full ${
                    item.priority === 'high' ? 'bg-gradient-to-r from-red-500 to-orange-500' :
                    item.priority === 'medium' ? 'bg-gradient-to-r from-yellow-500 to-amber-500' :
                    'bg-gradient-to-r from-blue-500 to-cyan-500'
                  }`} 
                  style={{ width: `${item.progress}%` }}
                ></div>
              </div>
              <p className="text-sm text-slate-400 mt-2">{item.progress}% complete</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );

  const renderAnalyticsTab = () => (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="metric-card text-center">
          <BarChart3 className="mx-auto mb-2 text-blue-500" size={24} />
          <div className="metric-value">24</div>
          <div className="metric-label">Interviews Taken</div>
        </div>
        
        <div className="metric-card text-center">
          <Trophy className="mx-auto mb-2 text-yellow-500" size={24} />
          <div className="metric-value">6.8</div>
          <div className="metric-label">Avg Score</div>
        </div>
        
        <div className="metric-card text-center">
          <Clock className="mx-auto mb-2 text-green-500" size={24} />
          <div className="metric-value">156h</div>
          <div className="metric-label">Practice Time</div>
        </div>
        
        <div className="metric-card text-center">
          <Target className="mx-auto mb-2 text-purple-500" size={24} />
          <div className="metric-value">87%</div>
          <div className="metric-label">Goal Progress</div>
        </div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900">
      {/* Header */}
      <header className="glass-panel border-b border-slate-700">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="bg-blue-500 p-2 rounded-lg">
                <Brain className="text-white" size={24} />
              </div>
              <div>
                <h1 className="text-xl font-bold text-white">CareerPilot</h1>
                <p className="text-slate-400 text-sm">Welcome back, {user?.name || 'Professional'}</p>
              </div>
            </div>
            
            <div className="flex items-center gap-4">
              <button 
                onClick={logout}
                className="btn-secondary py-2 px-4"
              >
                Sign Out
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <nav className="glass-panel border-b border-slate-700">
        <div className="container mx-auto px-4">
          <div className="flex space-x-8">
            {[
              { id: 'overview', label: 'Dashboard', icon: BarChart3 },
              { id: 'roadmap', label: 'Career Roadmap', icon: Compass },
              { id: 'analytics', label: 'Analytics', icon: TrendingUp }
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-4 px-2 border-b-2 font-medium text-sm flex items-center gap-2 transition-colors ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-400'
                    : 'border-transparent text-slate-400 hover:text-slate-300'
                }`}
              >
                <tab.icon size={18} />
                {tab.label}
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        {activeTab === 'overview' && renderOverviewTab()}
        {activeTab === 'roadmap' && renderRoadmapTab()}
        {activeTab === 'analytics' && renderAnalyticsTab()}
      </main>
    </div>
  );
};