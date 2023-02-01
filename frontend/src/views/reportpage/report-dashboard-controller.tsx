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
        const [scenJSON, handleFetchJSON] = useScenDataFromId(id)
        console.log(scenJSON)
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
                    <p className={
                        `mr-5 px-2 hover:bg-blue-300 hover:cursor-pointer" + ${activePage === 'base' ? ' bg-blue-500 text-white': 'bg-blue-100'}`
                    }
                        onClick={()=> setActivePage('base')}> Native load </p>
                    <p className={
                        `mr-5 px-2 hover:bg-blue-300 hover:cursor-pointer" + ${activePage === 'solar' ? ' bg-blue-500 text-white': 'bg-blue-100'}`
                    }
                        onClick={()=> setActivePage('solar')}> Solar </p>
                    <p className={
                        `mr-5 px-2 hover:bg-blue-300 hover:cursor-pointer" + ${activePage === 'storage' ? ' bg-blue-500 text-white': 'bg-blue-100'}`
                    }
                        onClick={()=> setActivePage('storage')}> Energy Storage </p>
                    <p className={
                        `mr-5 px-2 hover:bg-blue-300 hover:cursor-pointer" + ${activePage === 'ev' ? ' bg-blue-500 text-white': 'bg-blue-100'}`
                    }
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
                    activePage === 'storage' && scenJSON?.energy_storage?.length > 0 &&  <ESView 
                        batteryPower={batteryPower}
                        />
                }
                {
                    activePage === 'storage' && scenJSON?.energy_storage?.length == 0 && 
                    <div className="w-full h-96 flex justify-center
                    items-center">
                        <p className="text-4xl text-gray-500 border-b-2"> 
                            Energy Storage does not exist for this scenario. </p> 
                    </div>
                }
                    
                {
                    activePage === 'ev' && scenJSON?.ev?.length === 0 && <div className="w-full h-96 flex justify-center
                    items-center">
                        <p className="text-4xl text-gray-500 border-b-2"> EV does not exist in this scenario. </p> 
                    </div>
                }

                {
                    activePage === 'ev' && scenJSON?.ev?.length > 0 && <div className="w-full h-96 flex justify-center
                    items-center">
                        <p className="text-4xl text-gray-500 border-b-2"> Sorry we are still building EV model. </p> 
                    </div>
                }

                {
                    activePage === 'solar' && scenJSON?.solar?.length > 0 && <div className="w-full h-96 flex justify-center
                    items-center">
                        <p className="text-4xl text-gray-500 border-b-2"> Sorry we are still building Solar model. </p> 
                    </div>
                }

                {
                    activePage === 'solar' && scenJSON?.solar?.length === 0 && <div className="w-full h-96 flex justify-center
                    items-center">
                        <p className="text-4xl text-gray-500 border-b-2"> Solar does not exist in this scenario. </p> 
                    </div>
                }
                
            
            </div>
        );
}