import React, { useState } from 'react';
import { Button, TextField, Paper, Typography, Snackbar, CircularProgress } from '@material-ui/core';
import Alert from '@material-ui/lab/Alert';
import { useDispatch, useSelector } from 'react-redux';
import { triggerBuild, fetchBuildLogs } from '../store/buildSlice';

const BuildManager = () => {
  const dispatch = useDispatch();
  const [jobName, setJobName] = useState('');
  const [buildNumber, setBuildNumber] = useState('');
  const [log, setLog] = useState('');
  const [snackbar, setSnackbar] = useState({ open: false, severity: 'success', message: '' });
  const status = useSelector((state) => state.builds.status);
  
  const handleTrigger = () => {
    // Диспетчеризация действия для запуска сборки
    dispatch(triggerBuild(jobName)).then((result) => {
      if(result.payload && result.payload.success) {
        setSnackbar({ open: true, severity: 'success', message: 'Сборка запущена успешно!' });
      } else {
        setSnackbar({ open: true, severity: 'error', message: 'Ошибка при запуске сборки' });
      }
    }).catch((error) => {
      setSnackbar({ open: true, severity: 'error', message: error.message || 'Ошибка при запуске сборки' });
    });
  };

  const handleFetchLogs = () => {
    // Диспетчеризация действия для получения логов сборки
    dispatch(fetchBuildLogs({ jobName, buildNumber })).then((result) => {
      if(result.payload && result.payload.log) {
        setLog(result.payload.log);
        setSnackbar({ open: true, severity: 'success', message: 'Логи получены успешно' });
      } else {
        setLog('Логи не получены');
        setSnackbar({ open: true, severity: 'error', message: 'Ошибка при получении логов' });
      }
    }).catch((error) => {
      setSnackbar({ open: true, severity: 'error', message: error.message || 'Ошибка при получении логов' });
    });
  };

  return (
    <Paper style={{ padding: '1rem' }}>
      <Typography variant="h5" gutterBottom>
        Управление сборками
      </Typography>
      <TextField 
        label="Название задачи"
        variant="outlined"
        value={jobName}
        onChange={(e) => setJobName(e.target.value)}
        fullWidth
        style={{ marginBottom: '1rem' }}
      />
      <Button variant="contained" color="primary" onClick={handleTrigger} disabled={status === 'loading'}>
        {status === 'loading' ? <CircularProgress size={24} color="inherit" /> : 'Запустить сборку'}
      </Button>
      <br /><br />
      <TextField 
        label="Номер сборки"
        variant="outlined"
        value={buildNumber}
        onChange={(e) => setBuildNumber(e.target.value)}
        fullWidth
        style={{ marginBottom: '1rem' }}
      />
      <Button variant="contained" color="secondary" onClick={handleFetchLogs} disabled={status === 'loading'}>
        {status === 'loading' ? <CircularProgress size={24} color="inherit" /> : 'Получить логи сборки'}
      </Button>
      <br /><br />
      <Typography variant="body1">
        Логи сборки:
      </Typography>
      <Paper variant="outlined" style={{ maxHeight: 200, overflowY: 'auto', padding: '0.5rem' }}>
        <Typography variant="caption">
          {log}
        </Typography>
      </Paper>

      <Snackbar open={snackbar.open} autoHideDuration={6000} onClose={() => setSnackbar({ ...snackbar, open: false })}>
        <Alert onClose={() => setSnackbar({ ...snackbar, open: false })} severity={snackbar.severity} elevation={6} variant="filled">
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Paper>
  );
};

export default BuildManager; 