import React, {useState, useEffect} from 'react';
import axios from 'axios';
import { useSelector } from 'react-redux';
import { StateModel } from "../../interfaces/redux-state";
import { BaseLoadTSDataInterface } from '../../interfaces/report-interfaces';

const useTimeSeriesBaseLoad = (id:any): 
    [BaseLoadTSDataInterface| null, any, any] => {

    const [baseLoad, setBaseLoad] = useState<BaseLoadTSDataInterface| null>(null)
    const [baseEnergyMetrics, setBaseEnergyMetrics] = useState<any>(null)
    const [basePeakPowerMetrics, setBasePeakPowerMetrics] = useState<any>(null)
    
    const accessToken = useSelector(
        (state: StateModel) => state.auth.accessToken
    )
    const handleFetchLoadTSData = (id: number) => {
        axios.get(
            `/report/${id}/load/?data_type=base_timeseries`,
            { headers: { 'Authorization': 'Bearer ' + accessToken } }
        ).then((response) => {
            setBaseLoad(response.data)
        }).catch((error) => {
            if (error.response.status === 401) {
                localStorage.removeItem('state')
            }
        })
    }

    const handleFetchEnergyMetricsData = (id: number) => {
        axios.get(
            `/report/${id}/load/?data_type=base_energy_metrics`,
            { headers: { 'Authorization': 'Bearer ' + accessToken } }
        ).then((response) => {
            setBaseEnergyMetrics(response.data)
        }).catch((error) => {
            if (error.response.status === 401) {
                localStorage.removeItem('state')
            }
        })
    }

    const handleFetchPeakPowerData = (id: number) => {
        axios.get(
            `/report/${id}/load/?data_type=base_power_metrics`,
            { headers: { 'Authorization': 'Bearer ' + accessToken } }
        ).then((response) => {
            setBasePeakPowerMetrics(response.data)
        }).catch((error) => {
            if (error.response.status === 401) {
                localStorage.removeItem('state')
            }
        })
    }

    useEffect(()=> {
        handleFetchLoadTSData(id)
        handleFetchEnergyMetricsData(id)
        handleFetchPeakPowerData(id)
    }, [])

    return [baseLoad, baseEnergyMetrics, basePeakPowerMetrics]

}

export {useTimeSeriesBaseLoad}