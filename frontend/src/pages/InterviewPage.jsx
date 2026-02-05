import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Mic, 
  MicOff, 
  Play, 
  Pause, 
  RotateCcw, 
  AlertTriangle,
  Zap,
  Users,
  Clock,
  BarChart3,
  Brain,
  Target,
  CheckCircle,
  XCircle,
  Volume2,
  VolumeX
} from 'lucide-react';

export const InterviewPage = () => {
  const navigate = useNavigate();
  const [interviewState, setInterviewState] = useState('setup'); // setup, active, paused, completed
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [userAnswer, setUserAnswer] = useState('');
  const [timer, setTimer] = useState(0);
  const [isRecording, setIsRecording] = useState(false);
  const [pressureLevel, setPressureLevel] = useState('normal'); // normal, medium, high
  const [confidenceScore, setConfidenceScore] = useState(0);
  const [communicationScore, setCommunicationScore] = useState(0);

  // Mock interview data
  const mockQuestions = [
    {
      id: 1,
      text: "Explain the difference between SQL and NoSQL databases. When would you choose each?",
      category: "Database Design",
      difficulty: "medium",
      timeLimit: 180
    },
    {
      id: 2,
      text: "Describe a time when you had to debug a complex production issue. What was your approach?",
      category: "Problem Solving",
      difficulty: "medium",
      timeLimit: 240
    },
    {
      id: 3,
      text: "How would you design a scalable notification system that can handle millions of users?",
      category: "System Design",
      difficulty: "hard",
      timeLimit: 300
    }
  ];

  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);

  useEffect(() => {
    if (interviewState === 'active') {
      const interval = setInterval(() => {
        setTimer(prev => prev + 1);
      }, 1000);
      return () => clearInterval(interval);
    }
  }, [interviewState]);

  const startInterview = () => {
    setInterviewState('active');
    setCurrentQuestion(mockQuestions[0]);
    setTimer(0);
  };

  const nextQuestion = () => {
    if (currentQuestionIndex < mockQuestions.length - 1) {
      setCurrentQuestionIndex(prev => prev + 1);
      setCurrentQuestion(mockQuestions[currentQuestionIndex + 1]);
      setTimer(0);
      setUserAnswer('');
      
      // Simulate pressure increase based on performance
      if (currentQuestionIndex >= 1) {
        setPressureLevel('medium');
      }
      if (currentQuestionIndex >= 2) {
        setPressureLevel('high');
      }
    } else {
      finishInterview();
    }
  };

  const finishInterview = () => {
    setInterviewState('completed');
    // In real implementation, this would submit results and navigate to results page
    setTimeout(() => {
      navigate('/results');
    }, 2000);
  };

  const toggleRecording = () => {
    setIsRecording(!isRecording);
  };

  const handleSubmitAnswer = () => {
    // Simulate analysis
    const randomConfidence = Math.floor(Math.random() * 30) + 60; // 60-90
    const randomCommunication = Math.floor(Math.random() * 25) + 65; // 65-90
    
    setConfidenceScore(randomConfidence);
    setCommunicationScore(randomCommunication);
    
    nextQuestion();
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const getPressureColor = () => {
    switch (pressureLevel) {
      case 'high': return 'text-red-400';
      case 'medium': return 'text-yellow-400';
      default: return 'text-green-400';
    }
  };

  const getPressureIndicator = () => {
    switch (pressureLevel) {
      case 'high': return '🔴 High Pressure';
      case 'medium': return '🟡 Medium Pressure';
      default: return '🟢 Normal';
    }
  };

  if (interviewState === 'setup') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 p-4">
        <div className="max-w-4xl mx-auto">
          <div className="glass-panel p-8 rounded-xl text-center">
            <div className="mb-6">
              <div className="bg-blue-500 p-4 rounded-full w-16 h-16 mx-auto mb-4">
                <Brain className="text-white mx-auto" size={32} />
              </div>
              <h1 className="text-3xl font-bold text-white mb-2">Career Interview Assessment</h1>
              <p className="text-slate-400">Professional-grade interview simulation with real-time feedback</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              <div className="text-center">
                <Zap className="mx-auto mb-2 text-yellow-500" size={24} />
                <h3 className="font-semibold text-white mb-1">Real-time Analysis</h3>
                <p className="text-sm text-slate-400">Instant feedback on performance</p>
              </div>
              <div className="text-center">
                <Users className="mx-auto mb-2 text-blue-500" size={24} />
                <h3 className="font-semibold text-white mb-1">Pressure Simulation</h3>
                <p className="text-sm text-slate-400">Realistic interview conditions</p>
              </div>
              <div className="text-center">
                <Target className="mx-auto mb-2 text-green-500" size={24} />
                <h3 className="font-semibold text-white mb-1">Career Guidance</h3>
                <p className="text-sm text-slate-400">Personalized improvement paths</p>
              </div>
            </div>

            <button 
              onClick={startInterview}
              className="btn-primary px-8 py-4 text-lg flex items-center gap-2 mx-auto"
            >
              <Play size={24} />
              Begin Professional Interview
            </button>
          </div>
        </div>
      </div>
    );
  }

  if (interviewState === 'completed') {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-900 via-green-900 to-slate-900 p-4 flex items-center justify-center">
        <div className="glass-panel p-8 rounded-xl text-center max-w-md">
          <div className="mb-6">
            <div className="bg-green-500 p-4 rounded-full w-16 h-16 mx-auto mb-4">
              <CheckCircle className="text-white mx-auto" size={32} />
            </div>
            <h2 className="text-2xl font-bold text-white mb-2">Interview Complete!</h2>
            <p className="text-slate-300">Generating detailed analysis and feedback...</p>
          </div>
          <div className="loading-spinner mx-auto"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-900 p-4">
      <div className="max-w-6xl mx-auto">
        {/* Header with metrics */}
        <div className="glass-panel rounded-xl p-6 mb-6">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div className="flex items-center gap-4">
              <div className="flex items-center gap-2">
                <Clock className="text-blue-400" size={20} />
                <span className="text-white font-medium">{formatTime(timer)}</span>
              </div>
              <div className="flex items-center gap-2">
                <BarChart3 className={`${getPressureColor()} font-medium`} size={20} />
                <span className={getPressureColor()}>{getPressureIndicator()}</span>
              </div>
            </div>
            
            <div className="flex items-center gap-4">
              <div className="text-center">
                <div className="text-sm text-slate-400">Confidence</div>
                <div className="text-lg font-bold text-blue-400">{confidenceScore || '--'}%</div>
              </div>
              <div className="text-center">
                <div className="text-sm text-slate-400">Clarity</div>
                <div className="text-lg font-bold text-green-400">{communicationScore || '--'}%</div>
              </div>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Main Interview Panel */}
          <div className="lg:col-span-2 space-y-6">
            {/* Question Card */}
            <div className="interview-question">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-bold text-white">Question {currentQuestionIndex + 1} of {mockQuestions.length}</h2>
                <span className="badge badge-info">{currentQuestion?.category}</span>
              </div>
              <p className="text-lg text-slate-200 leading-relaxed">{currentQuestion?.text}</p>
              <div className="mt-4 flex items-center gap-2 text-sm text-slate-400">
                <Clock size={16} />
                <span>Time limit: {Math.floor(currentQuestion?.timeLimit / 60)} minutes</span>
              </div>
            </div>

            {/* Answer Input */}
            <div className="glass-card rounded-xl p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-lg font-semibold text-white">Your Response</h3>
                <button
                  onClick={toggleRecording}
                  className={`p-2 rounded-full ${
                    isRecording 
                      ? 'bg-red-500 hover:bg-red-600' 
                      : 'bg-slate-700 hover:bg-slate-600'
                  } transition-colors`}
                >
                  {isRecording ? <MicOff size={20} className="text-white" /> : <Mic size={20} className="text-white" />}
                </button>
              </div>
              
              <textarea
                value={userAnswer}
                onChange={(e) => setUserAnswer(e.target.value)}
                placeholder="Type or speak your answer here..."
                className="w-full h-48 p-4 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-500 focus:border-blue-500 focus:outline-none resize-none"
              />
              
              <div className="flex items-center justify-between mt-4">
                <div className="flex items-center gap-2 text-sm text-slate-400">
                  {isRecording && (
                    <>
                      <div className="w-3 h-3 bg-red-500 rounded-full animate-pulse"></div>
                      <span>Recording in progress...</span>
                    </>
                  )}
                </div>
                
                <div className="flex gap-3">
                  <button 
                    onClick={() => setUserAnswer('')}
                    className="btn-secondary py-2 px-4 flex items-center gap-2"
                  >
                    <RotateCcw size={16} />
                    Clear
                  </button>
                  <button 
                    onClick={handleSubmitAnswer}
                    disabled={!userAnswer.trim()}
                    className="btn-primary py-2 px-6 flex items-center gap-2 disabled:opacity-50"
                  >
                    <CheckCircle size={16} />
                    Submit Answer
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Sidebar with Real-time Analysis */}
          <div className="space-y-6">
            {/* Confidence Monitor */}
            <div className="glass-card rounded-xl p-6">
              <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                <Zap className="text-yellow-500" size={20} />
                Confidence Monitor
              </h3>
              <div className="space-y-3">
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-slate-400">Speech Clarity</span>
                    <span className="text-green-400">85%</span>
                  </div>
                  <div className="w-full bg-slate-700 rounded-full h-2">
                    <div className="bg-green-500 h-2 rounded-full" style={{ width: '85%' }}></div>
                  </div>
                </div>
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-slate-400">Filler Words</span>
                    <span className="text-blue-400">Low</span>
                  </div>
                  <div className="w-full bg-slate-700 rounded-full h-2">
                    <div className="bg-blue-500 h-2 rounded-full" style={{ width: '20%' }}></div>
                  </div>
                </div>
                <div>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-slate-400">Structure</span>
                    <span className="text-purple-400">Good</span>
                  </div>
                  <div className="w-full bg-slate-700 rounded-full h-2">
                    <div className="bg-purple-500 h-2 rounded-full" style={{ width: '75%' }}></div>
                  </div>
                </div>
              </div>
            </div>

            {/* Pressure Indicators */}
            <div className="glass-card rounded-xl p-6">
              <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
                <AlertTriangle className="text-orange-500" size={20} />
                Interview Dynamics
              </h3>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-slate-400">Pace</span>
                  <span className="text-green-400">Optimal</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-slate-400">Interruptions</span>
                  <span className="text-yellow-400">Moderate</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-slate-400">Depth Expected</span>
                  <span className="text-red-400">High</span>
                </div>
              </div>
            </div>

            {/* Quick Tips */}
            <div className="glass-card rounded-xl p-6">
              <h3 className="text-lg font-semibold text-white mb-4">Real-time Suggestions</h3>
              <ul className="space-y-2 text-sm">
                <li className="flex items-start gap-2">
                  <CheckCircle size={16} className="text-green-500 mt-0.5 flex-shrink-0" />
                  <span className="text-slate-300">Structure your response with clear introduction</span>
                </li>
                <li className="flex items-start gap-2">
                  <AlertTriangle size={16} className="text-yellow-500 mt-0.5 flex-shrink-0" />
                  <span className="text-slate-300">Watch your pace - you're speaking quickly</span>
                </li>
                <li className="flex items-start gap-2">
                  <Target size={16} className="text-blue-500 mt-0.5 flex-shrink-0" />
                  <span className="text-slate-300">Elaborate on the technical implementation details</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};