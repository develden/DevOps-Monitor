import { configureStore } from '@reduxjs/toolkit';
import buildReducer from './buildSlice';

const store = configureStore({
  reducer: {
    builds: buildReducer,
  },
});

export default store; 