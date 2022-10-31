import { Routes, Route} from "react-router-dom";
import {HomePage} from "./views/home-page";
import {Nav} from "./components/navigation-view";
import {ScenarioPage} from "./views/scenario-page";
import {DataUpload} from "./views/data-upload-page";
import {Login} from "./views/login-page";
import {DataPage} from "./views/datapage/data-page-controller";
import React, { Component } from 'react';
import axios from 'axios';
import {Config} from './helpers/config';
import {ErrorPage} from "./views/error-page-view";
import { Navigate, useLocation, Outlet, useNavigate} from "react-router-dom";
import {useSelector, useDispatch} from 'react-redux';
import {StateModel} from "./interfaces/redux-state";


axios.defaults.baseURL = Config.baseURL

// axios.interceptors.response.use(undefined, error => {
// })

const ProtectedRoutes = () => {

  const auth:any = useSelector( (state: StateModel) => state.auth)
  
  const location = useLocation()
  return auth?.user
              ? <Outlet/> 
              : <Navigate to="/login" state={{ from: location}} replace />
}

function App () {

    const navigation = useNavigate();
    const location = useLocation();
    const dispatch = useDispatch();


    return (
      <div>
        <Nav />
        <div>
          <Routes>
            <Route path='/login' element={<Login navigation={navigation} location={location} dispatch={dispatch}/>} />
            <Route element={<ProtectedRoutes/>}>
              <Route path='/' element={<HomePage navigation={navigation}/>} />
              <Route path='/scenarios' element={<ScenarioPage/>} />
              <Route path='/data' element={<DataPage/>} />
              <Route path='/data/upload' element={<DataUpload navigation={navigation}/>} />
            </Route>
            <Route path='*' element={<ErrorPage/>}/>
          </Routes>
        </div>
      </div>
    );
}

export default App;
