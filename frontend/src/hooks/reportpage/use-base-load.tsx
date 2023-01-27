import React, {useState, useEffect} from 'react';
import axios from 'axios';
import { useSelector } from 'react-redux';
import { StateModel } from "../../interfaces/redux-state";
import { BaseLoadTSDataInterface } from '../../interfaces/report-interfaces';

const useTimeSeriesBaseLoad = (id:any): 
    [BaseLoadTSDataInterface| null, any, any, any, any, any,
    any] => {

    const [baseLoad, setBaseLoad] = useState<BaseLoadTSDataInterface| null>(null)
    const [baseEnergyMetrics, setBaseEnergyMetrics] = useState<any>(null)
    const [basePeakPowerMetrics, setBasePeakPowerMetrics] = useState<any>(null)
    const [netLoad, setNetLoad] = useState<any>(null)
    const [netEnergyMetrics, setNetEnergyMetrics] = useState<any>(null)
    const [netPeakPowerMetrics, setNetPeakPowerMetrics] = useState<any>(null)
    const [batteryPower, setBatteryPower] = useState<any>(null)
    
    const accessToken = useSelector(
        (state: StateModel) => state.auth.accessToken
    )
    const handleFetchLoadTSData = (url: string, setter: React.Dispatch<any> ) => {
        axios.get(
            url,
            { headers: { 'Authorization': 'Bearer ' + accessToken } }
        ).then((response) => {
            setter(response.data)
        }).catch((error) => {
            if (error.response.status === 401) {
                localStorage.removeItem('state')
            }
        })
    }

    useEffect(()=> {
        handleFetchLoadTSData(`/report/${id}/load/?data_type=base_timeseries`, setBaseLoad)
        handleFetchLoadTSData(`/report/${id}/load/?data_type=base_energy_metrics`, setBaseEnergyMetrics )
        handleFetchLoadTSData(`/report/${id}/load/?data_type=base_power_metrics`, setBasePeakPowerMetrics)
        handleFetchLoadTSData(`/report/${id}/load/?data_type=net_timeseries`, setNetLoad)
        handleFetchLoadTSData(`/report/${id}/load/?data_type=net_energy_metrics`, setNetEnergyMetrics )
        handleFetchLoadTSData(`/report/${id}/load/?data_type=net_power_metrics`, setNetPeakPowerMetrics)
        handleFetchLoadTSData(`/report/${id}/load/?data_type=battery_power`, setBatteryPower)
    }, [])

    return [baseLoad, baseEnergyMetrics, basePeakPowerMetrics,
        netLoad, netEnergyMetrics, netPeakPowerMetrics, batteryPower]

}

export {useTimeSeriesBaseLoad}