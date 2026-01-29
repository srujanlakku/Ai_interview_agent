import { create } from 'zustand';
import { authAPI } from '../services/api';

export const useAuthStore = create((set) => ({
  user: null,
  token: localStorage.getItem('access_token') || null,
  isLoading: false,
  error: null,

  signup: async (email, fullName, password) => {
    set({ isLoading: true, error: null });
    try {
      const response = await authAPI.signup(email, fullName, password);
      set({ user: response.data, isLoading: false });
      return response.data;
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Signup failed';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  login: async (email, password) => {
    set({ isLoading: true, error: null });
    try {
      const response = await authAPI.login(email, password);
      const { access_token } = response.data;
      localStorage.setItem('access_token', access_token);
      set({ token: access_token, isLoading: false });
      return access_token;
    } catch (error) {
      const errorMessage = error.response?.data?.detail || 'Login failed';
      set({ error: errorMessage, isLoading: false });
      throw error;
    }
  },

  logout: async () => {
    localStorage.removeItem('access_token');
    set({ user: null, token: null });
    await authAPI.logout();
  },

  setError: (error) => set({ error }),
  clearError: () => set({ error: null }),
}));

export const useProfileStore = create((set) => ({
  profile: null,
  isLoading: false,
  error: null,

  setProfile: (profile) => set({ profile }),
  setLoading: (isLoading) => set({ isLoading }),
  setError: (error) => set({ error }),
}));

export const useInterviewStore = create((set) => ({
  currentInterview: null,
  interviews: [],
  isLoading: false,
  error: null,

  setCurrentInterview: (interview) => set({ currentInterview: interview }),
  setInterviews: (interviews) => set({ interviews }),
  setLoading: (isLoading) => set({ isLoading }),
  setError: (error) => set({ error }),
}));
