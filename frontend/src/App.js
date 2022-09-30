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
// import {Outlet} from "react-router"
import useAuth from "./hooks/useAuth";

axios.defaults.baseURL = Config.baseURL

const ProtectedRoutes = () => {
  const {auth} = useAuth();
  console.log('++++', auth)
  const location = useLocation()
  return auth?.user 
              ? <Outlet/> 
              : <Navigate to="/login" state={{ from: location}} replace />
}

function App () {
  const navigation = useNavigate();
  const location = useLocation();
  const { setAuth } = useAuth();

    return (
      <div>
        <Nav />
        <div class="px-20">
          <Routes>
            <Route path='/login' element={<Login navigation={navigation} location={location} setauth={setAuth}/>} />
            <Route element={<ProtectedRoutes />}>
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
