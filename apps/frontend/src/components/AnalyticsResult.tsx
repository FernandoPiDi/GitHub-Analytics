import ReactMarkdown from 'react-markdown';
import { markdownStyles } from '../utils/markdownStyles';

interface AnalyticsResultProps {
  explanation: string;
  elapsedTime: number;
}

export const AnalyticsResult = ({ explanation, elapsedTime }: AnalyticsResultProps) => {
  if (!explanation) return null;

  return (
    <div className="mt-6 bg-gray-50 dark:bg-gray-700 rounded-lg p-6 border border-gray-200 dark:border-gray-600">
      <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">Analysis Result</h2>
      <p className="text-sm text-gray-500 dark:text-gray-400 mb-4">Completed in {elapsedTime} seconds</p>
      <div className="prose prose-sm dark:prose-invert max-w-none">
        <ReactMarkdown
          components={{
            ...markdownStyles,
            code: ({node, inline, ...props}: {node?: any, inline?: boolean, [key: string]: any}) => 
              inline ? (
                <code className="bg-gray-100 dark:bg-gray-600 rounded px-1 py-0.5 font-mono text-sm" {...props} />
              ) : (
                <pre className="bg-gray-100 dark:bg-gray-600 rounded p-4 mb-4 overflow-x-auto">
                  <code {...props} />
                </pre>
              ),
          }}
        >
          {explanation}
        </ReactMarkdown>
      </div>
    </div>
  );
}; 
