import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { LoginPage } from './pages/LoginPage';
import { SignupPage } from './pages/SignupPage';
import { OnboardingPage } from './pages/OnboardingPage';
import { DashboardPage } from './pages/DashboardPage';
import { InterviewPage } from './pages/InterviewPage';
import './styles/globals.css';

function App() {
  // Create particle background effect
  useEffect(() => {
    const particleContainer = document.createElement('div');
    particleContainer.className = 'particle-bg';
    document.body.appendChild(particleContainer);
    
    // Create digital rain effect
    const digitalRain = document.createElement('div');
    digitalRain.className = 'digital-rain';
    document.body.appendChild(digitalRain);
    
    // Create scan line
    const scanLine = document.createElement('div');
    scanLine.className = 'scan-line';
    document.body.appendChild(scanLine);
    
    // Generate red particles
    for (let i = 0; i < 30; i++) {
      const particle = document.createElement('div');
      particle.className = 'particle';
      particle.style.left = `${Math.random() * 100}%`;
      particle.style.width = `${Math.random() * 3 + 1}px`;
      particle.style.height = particle.style.width;
      particle.style.animationDuration = `${Math.random() * 10 + 10}s`;
      particle.style.animationDelay = `${Math.random() * 5}s`;
      particleContainer.appendChild(particle);
    }
    
    // Generate yellow rain drops
    const rainContainer = document.createElement('div');
    rainContainer.className = 'yellow-rain-container';
    document.body.appendChild(rainContainer);
    
    for (let i = 0; i < 40; i++) {
      const rainDrop = document.createElement('div');
      rainDrop.className = 'yellow-rain-drop';
      rainDrop.style.left = `${Math.random() * 100}%`;
      rainDrop.style.animationDelay = `${Math.random() * 5}s`;
      rainDrop.style.animationDuration = `${Math.random() * 3 + 7}s`;
      rainDrop.style.opacity = `${Math.random() * 0.7 + 0.3}`;
      rainContainer.appendChild(rainDrop);
    }
    
    // Generate digital rain columns
    const characters = '01アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンABCDEFGHIJKLMNOPQRSTUVWXYZ';
    for (let i = 0; i < 30; i++) {
      const column = document.createElement('div');
      column.className = 'rain-column';
      column.style.left = `${i * 3.33}%`;
      column.style.animationDelay = `${Math.random() * 5}s`;
      column.style.animationDuration = `${Math.random() * 5 + 10}s`;
      
      let text = '';
      for (let j = 0; j < 20; j++) {
        text += characters.charAt(Math.floor(Math.random() * characters.length));
      }
      column.textContent = text;
      digitalRain.appendChild(column);
    }
    
    // Cleanup function
    return () => {
      document.body.removeChild(particleContainer);
      document.body.removeChild(digitalRain);
      document.body.removeChild(scanLine);
      if (document.querySelector('.yellow-rain-container')) {
        document.body.removeChild(document.querySelector('.yellow-rain-container'));
      }
    };
  }, []);
  
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Navigate to="/login" />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route path="/onboard" element={<OnboardingPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/interview" element={<InterviewPage />} />
      </Routes>
    </Router>
  );
}

export default App;
