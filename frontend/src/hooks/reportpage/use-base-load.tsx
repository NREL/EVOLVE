import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useSelector } from 'react-redux';
import { StateModel } from "../../interfaces/redux-state";
import { BaseLoadTSDataInterface } from '../../interfaces/report-interfaces';

const useTimeSeriesBaseLoad = (id: any):
    [BaseLoadTSDataInterface | null, any, any, any, any, any,
        any, any, any, any, any, any] => {

    const [baseLoad, setBaseLoad] = useState<BaseLoadTSDataInterface | null>(null)
    const [baseEnergyMetrics, setBaseEnergyMetrics] = useState<any>(null)
    const [basePeakPowerMetrics, setBasePeakPowerMetrics] = useState<any>(null)
    const [netLoad, setNetLoad] = useState<any>(null)
    const [netEnergyMetrics, setNetEnergyMetrics] = useState<any>(null)
    const [netPeakPowerMetrics, setNetPeakPowerMetrics] = useState<any>(null)
    const [batteryPower, setBatteryPower] = useState<any>(null)
    const [solarPower, setSolarPower] = useState<any>(null)
    const [solarMetrics, setSolarMetrics] = useState<any>(null)
    const [batteryDisChargMetrics, setBatteryDisChargMetrics] = useState<any>(null)
    const [batteryChargMetrics, setBatteryChargMetrics] = useState<any>(null)
    const [batterySOC, setBatterySOC] = useState<any>(null)

    const accessToken = useSelector(
        (state: StateModel) => state.auth.accessToken
    )
    const handleFetchLoadTSData = (url: string, setter: React.Dispatch<any>) => {
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

    useEffect(() => {
        handleFetchLoadTSData(`/report/${id}/load/?data_type=base_timeseries`, setBaseLoad)
        handleFetchLoadTSData(`/report/${id}/load/?data_type=base_energy_metrics`, setBaseEnergyMetrics)
        handleFetchLoadTSData(`/report/${id}/load/?data_type=base_power_metrics`, setBasePeakPowerMetrics)
        handleFetchLoadTSData(`/report/${id}/load/?data_type=net_timeseries`, setNetLoad)
        handleFetchLoadTSData(`/report/${id}/load/?data_type=net_energy_metrics`, setNetEnergyMetrics)
        handleFetchLoadTSData(`/report/${id}/load/?data_type=net_power_metrics`, setNetPeakPowerMetrics)
        handleFetchLoadTSData(`/report/${id}/load/?data_type=solar_power`, setSolarPower)
        handleFetchLoadTSData(`/report/${id}/load/?data_type=battery_power`, setBatteryPower)
        handleFetchLoadTSData(`/report/${id}/load/?data_type=solar_metrics`, setSolarMetrics)
        handleFetchLoadTSData(`/report/${id}/load/?data_type=battery_charging_metrics`, setBatteryChargMetrics)
        handleFetchLoadTSData(`/report/${id}/load/?data_type=battery_discharging_metrics`, setBatteryDisChargMetrics)
        handleFetchLoadTSData(`/report/${id}/load/?data_type=battery_soc`, setBatterySOC)
    }, [])

    return [baseLoad, baseEnergyMetrics, basePeakPowerMetrics,
        netLoad, netEnergyMetrics, netPeakPowerMetrics, batteryPower, solarPower,
        solarMetrics, batteryChargMetrics, batteryDisChargMetrics, batterySOC ]
}

export { useTimeSeriesBaseLoad }