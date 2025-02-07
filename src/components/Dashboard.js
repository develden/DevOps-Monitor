import React, { useState, useEffect } from 'react';
import { LineChart, Line, CartesianGrid, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { TextField, Paper, Typography } from '@material-ui/core';

const sampleData = [
  { name: 'Build 1', duration: 30 },
  { name: 'Build 2', duration: 45 },
  { name: 'Build 3', duration: 28 },
  { name: 'Build 4', duration: 50 },
  { name: 'Build 5', duration: 35 },
];

const Dashboard = () => {
  const [data, setData] = useState(sampleData);
  const [filter, setFilter] = useState('');

  useEffect(() => {
    // Здесь можно выполнить асинхронный запрос к API backend для получения данных сборок
    // Например: fetch('/api/builds').then(r => r.json()).then(setData);
  }, []);

  const handleFilterChange = (e) => {
    setFilter(e.target.value);
    // Примените фильтрацию к данным по необходимости. Здесь фильтруем по имени сборки.
    const filtered = sampleData.filter(item => item.name.toLowerCase().includes(e.target.value.toLowerCase()));
    setData(filtered);
  };

  return (
    <Paper style={{ padding: '1rem' }}>
      <Typography variant="h5" gutterBottom>
        Дашборд сборок
      </Typography>
      <TextField 
        label="Поиск сборок"
        variant="outlined"
        value={filter}
        onChange={handleFilterChange}
        fullWidth
        style={{ marginBottom: '1rem' }}
      />
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={data}>
          <Line type="monotone" dataKey="duration" stroke="#8884d8" />
          <CartesianGrid stroke="#ccc" />
          <XAxis dataKey="name" />
          <YAxis label={{ value: 'Время (сек)', angle: -90, position: 'insideLeft' }} />
          <Tooltip />
        </LineChart>
      </ResponsiveContainer>
    </Paper>
  );
};

export default Dashboard; 