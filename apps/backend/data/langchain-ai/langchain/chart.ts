import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { DatePicker, Space } from 'antd';
import 'antd/dist/antd.css';
import fs from 'fs';

// Define the type for commit data
interface CommitData {
    date: string;
    commit_count: number;
}

const App: React.FC = () => {
    const [data, setData] = useState<CommitData[]>([]);
    const [filteredData, setFilteredData] = useState<CommitData[]>([]);
    const [startDate, setStartDate] = useState<string | null>(null);
    const [endDate, setEndDate] = useState<string | null>(null);

    useEffect(() => {
        // Load commit data from JSON file
        fs.readFile('./data.json', 'utf8', (err, jsonString) => {
            if (err) {
                console.error("Failed to read file:", err);
                return;
            }
            try {
                const rawData = JSON.parse(jsonString);
                const transformedData: CommitData[] = rawData.map((d: any) => ({
                    date: new Date(d.committed_date).toISOString().split('T')[0],
                    commit_count: 1, // assuming each entry is a single commit
                })).reduce((acc: CommitData[], current: CommitData) => {
                    const existingDate = acc.find(item => item.date === current.date);
                    if (existingDate) {
                        existingDate.commit_count += 1;
                    } else {
                        acc.push(current);
                    }
                    return acc;
                }, []);
                setData(transformedData);
                setFilteredData(transformedData);
            } catch (err) {
                console.error("Failed to parse JSON data:", err);
            }
        });
    }, []);

    const onDateChange = (dates: [moment.Moment, moment.Moment] | null) => {
        if (dates) {
            const start = dates[0].format('YYYY-MM-DD');
            const end = dates[1].format('YYYY-MM-DD');
            setStartDate(start);
            setEndDate(end);
            setFilteredData(data.filter(d => d.date >= start && d.date <= end));
        } else {
            setFilteredData(data);
        }
    };

    return (
        <div>
            <h1>Commit History</h1>
            <Space direction="vertical" size={12}>
                <DatePicker.RangePicker onChange={onDateChange} />
            </Space>
            <ResponsiveContainer width="100%" height={400}>
                <LineChart data={filteredData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Line type="monotone" dataKey="commit_count" stroke="#8884d8" />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
};

export default App;