import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
  LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid
} from 'recharts';

interface CommitData {
  date: string;
  commits: number;
}

const Chart: React.FC = () => {
  const [data, setData] = useState<CommitData[]>([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('/charts/langchain-ai/langchain/data.json');
        const rawData = response.data;

        const formattedData = rawData.reduce((acc: CommitData[], commit: any) => {
          const date = commit.committed_date.split('T')[0];
          const existingDate = acc.find(item => item.date === date);
          if (existingDate) {
            existingDate.commits += 1;
          } else {
            acc.push({ date, commits: 1 });
          }
          return acc;
        }, []).sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());

        const lastWeekData = formattedData.slice(-7);

        setData(lastWeekData);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip formatter={(value) => `${value} commits`} />
        <Line type="monotone" dataKey="commits" stroke="#8884d8" />
      </LineChart>
    </ResponsiveContainer>
  );
};

export default Chart;