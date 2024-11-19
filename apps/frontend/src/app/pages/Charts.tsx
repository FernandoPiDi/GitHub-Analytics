import React, { useEffect } from 'react';
import CommitsChart from '../charts/langchain-ai/langchain/chart';

interface ChartsProps {
  shouldRefresh: boolean;
  onRefreshComplete: () => void;
  owner: string;
  repo: string;
}

export function Charts({ shouldRefresh, onRefreshComplete, owner, repo }: ChartsProps) {
  useEffect(() => {
    if (shouldRefresh) {
      onRefreshComplete();
    }
  }, [shouldRefresh, onRefreshComplete]);

  return (
    <div className="bg-white dark:bg-gray-800 shadow-sm rounded-lg p-6 h-full flex flex-col">
      <div className="mb-6">
        <h2 className="text-2xl font-semibold text-gray-900 dark:text-white">Resulting chart for {owner}/{repo}</h2>
      </div>

      <div className="flex-1">
        <div className="bg-gray-50 dark:bg-gray-700 rounded-lg p-6 border border-gray-200 dark:border-gray-600 h-full">
          <div className="h-full">
            <CommitsChart key={`${owner}-${repo}-${shouldRefresh}`}/>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Charts; 
