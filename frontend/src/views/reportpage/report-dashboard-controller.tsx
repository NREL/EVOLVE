import React from 'react';
import { useTimeSeriesBaseLoad } from '../../hooks/reportpage/use-base-load';
import { useScenDataFromId } from '../../hooks/reportpage/use-single-scen';
import { useParams } from 'react-router-dom';
import { NativeLoadView} from './native-load-view';

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
        const [baseLoad, baseEnergyMetrics, basePeakPowerMetrics]  = useTimeSeriesBaseLoad(id)
        const [scenJSON, handleFetchJSON] = useScenDataFromId(2)
        

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
                    <p className="mr-5 bg-blue-100 px-2 hover:bg-blue-300 hover:cursor-pointer"> Native load </p>
                    <p className="mr-5 bg-blue-100 px-2 hover:bg-blue-300 hover:cursor-pointer"> Solar </p>
                    <p className="mr-5 bg-blue-100 px-2 hover:bg-blue-300 hover:cursor-pointer"> Energy Storage </p>
                    <p className="mr-5 bg-blue-100 px-2 hover:bg-blue-300 hover:cursor-pointer"> Electric Vehicle </p>
                </div>

                <NativeLoadView 
                    baseLoad={baseLoad}
                    baseEnergyMetrics={baseEnergyMetrics}
                    basePeakPowerMetrics={basePeakPowerMetrics}
                />
            
            </div>
        );
}