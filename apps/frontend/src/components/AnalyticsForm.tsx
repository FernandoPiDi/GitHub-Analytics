import { AnalyticsFormData } from '../types';

interface AnalyticsFormProps {
  formData: AnalyticsFormData;
  isLoading: boolean;
  elapsedTime: number;
  onSubmit: (e: React.FormEvent) => void;
  onChange: (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => void;
}

export const AnalyticsForm = ({ 
  formData, 
  isLoading, 
  elapsedTime, 
  onSubmit, 
  onChange 
}: AnalyticsFormProps) => {
  return (
    <form onSubmit={onSubmit} className="space-y-6">
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Message</label>
        <textarea
          name="message"
          value={formData.message}
          onChange={onChange}
          className="mt-1 block w-full rounded-md border-gray-300 dark:border-gray-600 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:text-white sm:text-sm"
          rows={4}
          required
        />
      </div>

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
        {/* Owner and Repo inputs */}
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Owner</label>
          <input
            type="text"
            name="owner"
            value={formData.owner}
            onChange={onChange}
            className="mt-1 block w-full rounded-md border-gray-300 dark:border-gray-600 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:text-white sm:text-sm"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Repository</label>
          <input
            type="text"
            name="repo"
            value={formData.repo}
            onChange={onChange}
            className="mt-1 block w-full rounded-md border-gray-300 dark:border-gray-600 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:text-white sm:text-sm"
            required
          />
        </div>
      </div>

      {/* GitHub PAT input and submit button */}
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">GitHub PAT</label>
        <input
          type="password"
          name="ghPat"
          value={formData.ghPat}
          onChange={onChange}
          className="mt-1 block w-full rounded-md border-gray-300 dark:border-gray-600 shadow-sm focus:border-blue-500 focus:ring-blue-500 dark:bg-gray-700 dark:text-white sm:text-sm"
          required
        />
      </div>

      <div>
        <button 
          type="submit"
          className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:bg-blue-300 disabled:cursor-not-allowed"
          disabled={isLoading}
        >
          {isLoading ? (
            <div className="flex items-center gap-2">
              <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              <span>Analyzing... ({elapsedTime}s)</span>
            </div>
          ) : (
            'Analyze Repository'
          )}
        </button>
      </div>
    </form>
  );
}; 
