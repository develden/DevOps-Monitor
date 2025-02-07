import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

// Асинхронное действие для запуска сборки
export const triggerBuild = createAsyncThunk(
  'builds/triggerBuild',
  async (jobName) => {
    // Выполните запрос к backend API для запуска сборки
    const response = await fetch(`/api/trigger-build`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ jobName }),
    });
    const data = await response.json();
    return data;
  }
);

// Асинхронное действие для получения логов сборки
export const fetchBuildLogs = createAsyncThunk(
  'builds/fetchBuildLogs',
  async ({ jobName, buildNumber }) => {
    // Запрос к API для получения логов сборки
    const response = await fetch(`/api/build-logs?jobName=${jobName}&buildNumber=${buildNumber}`);
    const data = await response.json();
    return data;
  }
);

const buildSlice = createSlice({
  name: 'builds',
  initialState: {
    builds: [],
    logs: '',
    status: 'idle',
    error: null,
  },
  reducers: {
    // Дополнительные редьюсеры при необходимости
  },
  extraReducers: (builder) => {
    builder
      .addCase(triggerBuild.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(triggerBuild.fulfilled, (state, action) => {
        state.status = 'succeeded';
      })
      .addCase(triggerBuild.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.error.message;
      })
      .addCase(fetchBuildLogs.pending, (state) => {
        state.status = 'loading';
      })
      .addCase(fetchBuildLogs.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.logs = action.payload.log;
      })
      .addCase(fetchBuildLogs.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.error.message;
      });
  },
});

export default buildSlice.reducer; 