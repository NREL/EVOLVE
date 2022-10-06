import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import { BrowserRouter} from "react-router-dom";
import App from './App';
import reportWebVitals from './reportWebVitals';
import {configureStore} from '@reduxjs/toolkit';
import rootReducer from './reducers';
import { Provider } from 'react-redux';
import { loadState, saveState } from './localStorage';


const preloadedState = loadState();
console.log('hello', preloadedState)
const store = configureStore({
  reducer: rootReducer,
  preloadedState
  }
)

store.subscribe(() => {
  console.log(store.getState())
  saveState(store.getState());
});

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <Provider store={store}>
    <React.StrictMode>
      <BrowserRouter>
          <App />
      </BrowserRouter>
    </React.StrictMode>
  </Provider>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
