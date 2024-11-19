import { Route, Routes } from 'react-router-dom';
import { useState, useEffect } from 'react';
import axios from 'axios';
import Charts from './pages/Charts';
import { Navigation } from '../components/Navigation';
import { AnalyticsForm } from '../components/AnalyticsForm';
import { AnalyticsResult } from '../components/AnalyticsResult';
import { AnalyticsFormData } from '../types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export function App() {
  const [formData, setFormData] = useState<AnalyticsFormData>({
    message: '',
    owner: '',
    repo: '',
    ghPat: ''
  });
  const [explanation, setExplanation] = useState<string>('');
  const [error, setError] = useState<string>('');
  const [isLoading, setIsLoading] = useState(false);
  const [elapsedTime, setElapsedTime] = useState(0);
  const [timerInterval, setTimerInterval] = useState<NodeJS.Timeout | null>(null);
  const [darkMode, setDarkMode] = useState(() => {
    if (typeof window !== 'undefined') {
      const savedMode = localStorage.getItem('darkMode');
      return savedMode ? JSON.parse(savedMode) : 
             window.matchMedia('(prefers-color-scheme: dark)').matches;
    }
    return false;
  });
  const [shouldRefreshChart, setShouldRefreshChart] = useState(false);

  useEffect(() => {
    return () => {
      if (timerInterval) {
        clearInterval(timerInterval);
      }
    };
  }, [timerInterval]);

  useEffect(() => {
    document.documentElement.classList.toggle('dark', darkMode);
    localStorage.setItem('darkMode', JSON.stringify(darkMode));
  }, [darkMode]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setExplanation('');
    setIsLoading(true);
    setElapsedTime(0);

    const interval = setInterval(() => {
      setElapsedTime(prev => prev + 1);
    }, 1000);
    setTimerInterval(interval);

    try {
      const response = await axios.post(`${API_URL}/v1/analytics`, 
        {
          message: formData.message,
          owner: formData.owner,
          repo: formData.repo
        },
        {
          headers: {
            'x-gh-pat': formData.ghPat
          }
        }
      );
      setExplanation(response.data.explanation);
      setShouldRefreshChart(true);
    } catch (err) {
      setError('Failed to fetch data. Please try again.');
      console.error('Error:', err);
    } finally {
      setIsLoading(false);
      if (interval) {
        clearInterval(interval);
      }
      setTimerInterval(null);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Navigation darkMode={darkMode} setDarkMode={setDarkMode} />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="flex flex-col lg:flex-row gap-5 h-full">
          {/* Form Section */}
          <div className="lg:w-1/2 lg:h-full">
            <div className="bg-white dark:bg-gray-800 shadow-sm rounded-lg p-6 h-full">
              <AnalyticsForm
                formData={formData}
                isLoading={isLoading}
                elapsedTime={elapsedTime}
                onSubmit={handleSubmit}
                onChange={handleInputChange}
              />

              {error && (
                <div className="mt-6 rounded-md bg-red-50 p-4">
                  <div className="flex">
                    <div className="flex-shrink-0">
                      <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                      </svg>
                    </div>
                    <div className="ml-3">
                      <p className="text-sm font-medium text-red-800">{error}</p>
                    </div>
                  </div>
                </div>
              )}

              <AnalyticsResult explanation={explanation} elapsedTime={elapsedTime} />
            </div>
          </div>

          {/* Charts Section */}
          <div className="lg:w-1/2 lg:h-full">
            <Charts 
              shouldRefresh={shouldRefreshChart} 
              onRefreshComplete={() => setShouldRefreshChart(false)}
              owner={formData.owner}
              repo={formData.repo}
            />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
