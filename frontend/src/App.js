import { Routes, Route} from "react-router-dom";
import {HomePage} from "./views/HomePage";
import {Nav} from "./components/Navigation";
import {ScenarioPage} from "./views/ScenarioPage";
import {DataUpload} from "./views/DataUploadPage";
import {Login} from "./views/LoginPage";
import {DataPage} from "./views/DataPage";
import React, { Component } from 'react';
import axios from 'axios';
import {Config} from './Config';
import {ErrorPage} from "./views/ErrorPage";
import { Navigate, useLocation, Outlet, useNavigate} from "react-router-dom";
import {useSelector, useDispatch} from 'react-redux';
 
axios.defaults.baseURL = Config.baseURL

const ProtectedRoutes = () => {

  const auth = useSelector(state => state.auth)
  console.log('auth', auth)
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
        <div class="px-20">
          <Routes>
            <Route path='/login' element={<Login navigation={navigation} location={location} dispatch={dispatch}/>} />
            <Route element={<ProtectedRoutes/>}>
              <Route path='/' element={<HomePage navigation={navigation}/>} />
              <Route path='/scenarios' element={<ScenarioPage/>} />
              <Route path='/data' element={<DataPage navigation={navigation}/>} />
              <Route path='/data/upload' element={<DataUpload navigation={navigation}/>} />
            </Route>
            <Route path='*' element={<ErrorPage/>}/>
          </Routes>
        </div>
      </div>
    );
}

export default App;
