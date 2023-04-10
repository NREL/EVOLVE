import React, { useState } from 'react';
import { useTimeSeriesBaseLoad } from '../../hooks/reportpage/use-base-load';
import { useScenDataFromId } from '../../hooks/reportpage/use-single-scen';
import { useParams } from 'react-router-dom';
import { NativeLoadView } from './native-load-view';
import { TimeseriesPowerView } from './timeseries-power-view';
import fileDownload from 'js-file-download';
import axios from 'axios';
import { StateModel } from "../../interfaces/redux-state";
import { useSelector } from 'react-redux';
import { EnergyMetricsView } from './energy-metrics-view';


export const ReportDashboardController: React.FC = () => {

    const { id } = useParams();
    const accessToken = useSelector((state: StateModel) => state.auth.accessToken);

    const [baseLoad, baseEnergyMetrics, basePeakPowerMetrics,
        netLoad, netEnergyMetrics, netPeakPowerMetrics, batteryPower,
        solarPower, solarMetrics, batteryChargMetrics, batteryDisChargMetrics,
        batterySOC
    ] = useTimeSeriesBaseLoad(id);

    const handleDataDownload = (id: any) => {
        axios.get(`/report/${id}/file`,
            { headers: { 'Authorization': 'Bearer ' + accessToken }, responseType: 'blob' }
        ).then((response) => {
            console.log(response)
            fileDownload(response.data, `${id}.zip`)
        })
    };

    const [scenJSON, handleFetchJSON] = useScenDataFromId(id);
    const [activePage, setActivePage] = useState('Native load');
    const pages = ['Native load', 'Solar', 'Energy Storage', 'Electric Vehicle']


    return (
        <div className="mx-10 my-5">

            {
                <p className="text-blue-500 font-bold pb-3"> <span> Scenario {'>>'} </span>
                    <span> {scenJSON?.basic?.scenarioName} {'>>'} </span>
                    <span> Report {'>>'} </span>
                    <span> Report 1 </span>
                </p>
            }

            <div>
                <p className='text-white px-2 rounded-md bg-orange-500 mb-5
                w-max py-1 font-bold hover:cursor-pointer hover:bg-orange-700'
                    onClick={() => handleDataDownload(id)}
                > Download results !</p>
            </div>

            <div className="flex border-b border-blue-500 mb-5">
                {
                    pages.map((item: string) => {
                        return <p className={
                            `mr-5 px-2 hover:bg-blue-300 hover:cursor-pointer" 
                            + ${activePage === item ? ' bg-blue-500 text-white' : 'bg-blue-100'}`
                        }
                            onClick={() => setActivePage(item)}> {item} </p>
                    })
                }

            </div>

            {
                activePage === 'Native load' && <NativeLoadView
                    baseLoad={baseLoad}
                    baseEnergyMetrics={baseEnergyMetrics}
                    basePeakPowerMetrics={basePeakPowerMetrics}
                    netLoad={netLoad}
                    netEnergyMetrics={netEnergyMetrics}
                    netPeakPowerMetrics={netPeakPowerMetrics} />
            }

            {
                activePage === 'Energy Storage' && scenJSON?.energy_storage?.length > 0 && 
                
                <div>
                    <div className='flex'>
                        <EnergyMetricsView 
                            metric={batteryChargMetrics}
                            title={"Charging Energy (kWh)"}
                        />
                        <EnergyMetricsView 
                            metric={batteryDisChargMetrics}
                            title={"Discharging Energy (kWh)"}
                        />
                    </div>
                    <TimeseriesPowerView
                        tsPower={batteryPower}
                        title={'kW Profile'}
                    />
                    <TimeseriesPowerView
                        tsPower={batterySOC}
                        title={'State of Charge'}
                    />
                </div>
                
            }
            {
                activePage === 'Energy Storage' && scenJSON?.energy_storage?.length == 0 &&
                <div className="w-full h-96 flex justify-center
                    items-center">
                    <p className="text-4xl text-gray-500 border-b-2">
                        Energy Storage does not exist for this scenario. </p>
                </div>
            }

            {
                activePage === 'Electric Vehicle' && scenJSON?.ev?.length === 0 &&
                <div className="w-full h-96 flex justify-center
                    items-center">
                    <p className="text-4xl text-gray-500 border-b-2"> EV does not
                        exist in this scenario. </p>
                </div>
            }

            {
                activePage === 'Electric Vehicle' && scenJSON?.ev?.length > 0 &&
                <div className="w-full h-96 flex justify-center
                        items-center">
                    <p className="text-4xl text-gray-500 border-b-2"> Sorry we are
                        still building EV model. </p>
                </div>
            }

            {

                activePage === 'Solar' && scenJSON?.solar?.length > 0 &&
                <div>
                    <EnergyMetricsView 
                        metric={solarMetrics}
                        title={"Solar Energy Generation (kWh)"}
                    />
                    <TimeseriesPowerView
                        tsPower={solarPower}
                        title={'kW Profile'}
                    />
                </div>
            }

            {
                activePage === 'Solar' && scenJSON?.solar?.length === 0 &&
                <div className="w-full h-96 flex justify-center
                        items-center">
                    <p className="text-4xl text-gray-500 border-b-2"> Solar 
                    does not exist in this scenario. </p>
                </div>
            }


        </div>
    );
}