import React, { useState } from 'react';
import { useTimeSeriesBaseLoad } from '../../hooks/reportpage/use-base-load';
import { useScenDataFromId } from '../../hooks/reportpage/use-single-scen';
import { useParams } from 'react-router-dom';
import { NativeLoadView} from './native-load-view';
import { ESView } from './energy-storage-view';

interface ReportDashboardControllerProps {

}

const getDateTimeList = (
    start_date: string,
    resolution: number,
    length_: number,
) => {
    let timestamps = []
    for (let i=0; i < length_; i++) {
        timestamps.push(new Date(new Date(start_date).getTime() 
        + i*resolution*60000))
    }

    return timestamps
}


export const ReportDashboardController: React.FC<ReportDashboardControllerProps> = ({

}) => {

        const {id} = useParams();
        const [baseLoad, baseEnergyMetrics, basePeakPowerMetrics,
            netLoad, netEnergyMetrics, netPeakPowerMetrics, batteryPower ]  = useTimeSeriesBaseLoad(id)
        const [scenJSON, handleFetchJSON] = useScenDataFromId(2)
        const [activePage, setActivePage] = useState('base')
    

        return (
            <div className="mx-10 my-5">

                {/* {
                    <p className="text-blue-500 font-bold pb-3"> <span> Scenario {'>>'} </span> 
                    <span> {scenJSON?.basic?.scenarioName } {'>>'} </span>
                    <span> Report {'>>'} </span>
                    <span> Report 1 </span>
                    </p>
                } */}
                <div className="flex border-b border-blue-500 mb-5">
                    <p className="mr-5 bg-blue-100 px-2 hover:bg-blue-300 hover:cursor-pointer"
                        onClick={()=> setActivePage('base')}> Native load </p>
                    <p className="mr-5 bg-blue-100 px-2 hover:bg-blue-300 hover:cursor-pointer"
                        onClick={()=> setActivePage('solar')}> Solar </p>
                    <p className="mr-5 bg-blue-100 px-2 hover:bg-blue-300 hover:cursor-pointer"
                        onClick={()=> setActivePage('storage')}> Energy Storage </p>
                    <p className="mr-5 bg-blue-100 px-2 hover:bg-blue-300 hover:cursor-pointer"
                        onClick={()=> setActivePage('ev')}> Electric Vehicle </p>
                </div>

                {
                    activePage === 'base' && <NativeLoadView 
                    baseLoad={baseLoad}
                    baseEnergyMetrics={baseEnergyMetrics}
                    basePeakPowerMetrics={basePeakPowerMetrics}
                    netLoad={netLoad}
                    netEnergyMetrics={netEnergyMetrics}
                    netPeakPowerMetrics={netPeakPowerMetrics} />
                }
                
                {
                    activePage === 'storage' && <ESView 
                        batteryPower={batteryPower}
                    />
                }
                
            
            </div>
        );
}