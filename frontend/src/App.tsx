import { Routes, Route } from "react-router-dom";
import { HomePage } from "./views/home-page";
import { Nav } from "./components/navigation-view";
import ScenarioPageController from "./views/scenariopage/scenario-page-controller";
import { DataUpload } from "./views/data-upload-page";
import { Login } from "./views/login-page";
import { SignUpPage } from "./views/sign-up-page";
import { DataPage } from "./views/datapage/data-page-controller";
import React, { Component } from 'react';
import axios from 'axios';
// import { Config } from './helpers/config';
import { ErrorPage } from "./views/error-page-view";
import { Navigate, useLocation, Outlet, useNavigate } from "react-router-dom";
import { useSelector, useDispatch } from 'react-redux';
import { StateModel } from "./interfaces/redux-state";
import { CreateScenario } from "./views/createscenariopage/create-scenario-controller";
import { LabelPageController } from "./views/labelpage/label-page-controller";
import { ReportDashboardController } from "./views/reportpage/report-dashboard-controller";


axios.defaults.baseURL = process.env.REACT_APP_EVOLVE_BACKEND_URL; //Config.baseURL
// axios.interceptors.response.use(undefined, error => {
// })

console.log(axios.defaults.baseURL, '---')

const ProtectedRoutes = () => {

  const auth: any = useSelector((state: StateModel) => state.auth)

  const location = useLocation()
  return auth?.user
    ? <Outlet />
    : <Navigate to="/login" state={{ from: location }} replace />
}

function App() {

  const navigation = useNavigate();
  const location = useLocation();
  const dispatch = useDispatch();


  return (
    <div>
      <Nav />
      <div>
        <Routes>
          <Route path='/login' element={<Login navigation={navigation} location={location} dispatch={dispatch} />} />
          <Route path='/signup' element={<SignUpPage />} />
          <Route element={<ProtectedRoutes />}>
            <Route path='/' element={<HomePage navigation={navigation} />} />
            <Route path='/scenarios' element={<ScenarioPageController />} />
            <Route path='/create-scenario' element={<CreateScenario navigation={navigation} />} />
            <Route path='/data' element={<DataPage />} />
            <Route path='/labels' element={<LabelPageController />} />
            <Route path='/data/upload' element={<DataUpload navigation={navigation} />} />
            <Route path='/report/:id' element={<ReportDashboardController />} />
          </Route>
          <Route path='*' element={<ErrorPage />} />
        </Routes>
      </div>
    </div>
  );
}

export default App;
