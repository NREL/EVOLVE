import React from 'react';
import ReactDOM from 'react-dom';
import $ from 'jquery';
import Popper from 'popper.js';
import 'bootstrap/dist/js/bootstrap.bundle.min';
import 'bootstrap/dist/css/bootstrap.css';
import {BrowserRouter, Route} from 'react-router-dom'
import './index.css';
import * as serviceWorker from './serviceWorker';
import App from './app/App';
import User from './app/auth/User';
import Profile from './app/Profile/Profile';

ReactDOM.render(
  <BrowserRouter>
      <switch>
          <Route 
            exact 
            path={'/'} 
            render = { props => <User {...props}/>}
          />
          <Route 
            exact 
            path={'/dashboard'} 
            render = { props => <App {...props}/>}
          />
          <Route 
            exact 
            path={'/profile'} 
            render = { props => <Profile {...props}/>}
          />
      </switch>
  </BrowserRouter> ,
  document.getElementById('root')
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
