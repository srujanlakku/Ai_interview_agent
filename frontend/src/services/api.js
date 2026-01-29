import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle response errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  signup: (email, fullName, password) =>
    apiClient.post('/auth/signup', { email, full_name: fullName, password }),
  login: (email, password) =>
    apiClient.post('/auth/login', { email, password }),
  logout: () => {
    localStorage.removeItem('access_token');
    return Promise.resolve();
  },
};

// Profile API
export const profileAPI = {
  onboard: (userId, profile) =>
    apiClient.post(`/profile/onboard?user_id=${userId}`, profile),
  getProfile: (userId) =>
    apiClient.get(`/profile/${userId}`),
  generatePreparation: (userId) =>
    apiClient.post(`/profile/${userId}/prepare`),
};

// Interview API
export const interviewAPI = {
  createInterview: (userId, interviewData) =>
    apiClient.post(`/interviews/create?user_id=${userId}`, interviewData),
  getInterview: (interviewId, userId) =>
    apiClient.get(`/interviews/${interviewId}?user_id=${userId}`),
  getUserInterviews: (userId) =>
    apiClient.get(`/interviews/user/${userId}/list`),
  getStatistics: (userId) =>
    apiClient.get(`/interviews/${userId}/statistics`),
  startQuestion: (interviewId, userId) =>
    apiClient.post(`/interviews/${interviewId}/start-question?user_id=${userId}`),
  submitAnswer: (interviewId, userId, questionId, answer) =>
    apiClient.post(`/interviews/${interviewId}/submit-answer`, {
      user_id: userId,
      question_id: questionId,
      answer,
    }),
  finalizeInterview: (interviewId, userId) =>
    apiClient.post(`/interviews/${interviewId}/finalize?user_id=${userId}`),
};

// Memory API
export const memoryAPI = {
  getSummary: (userId) =>
    apiClient.get(`/memory/${userId}/summary`),
  getStrengths: (userId) =>
    apiClient.get(`/memory/${userId}/strengths`),
  getWeaknesses: (userId) =>
    apiClient.get(`/memory/${userId}/weaknesses`),
  getCoveredTopics: (userId) =>
    apiClient.get(`/memory/${userId}/covered-topics`),
  getMissedTopics: (userId) =>
    apiClient.get(`/memory/${userId}/missed-topics`),
};

export default apiClient;
