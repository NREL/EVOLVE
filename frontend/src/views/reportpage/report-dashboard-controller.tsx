import React, { useState, useEffect } from 'react'
import axios from 'axios';
import { useSelector } from 'react-redux';
import { StateModel } from "../../interfaces/redux-state";
import Plot from 'react-plotly.js';


interface ReportDashboardControllerProps {

}

interface BaseLoadTSDataInterface {
    data: number[];
    start_date: string;
    end_date: string;
    resolution: number;
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

        const [baseLoad, setBaseLoad] = useState<BaseLoadTSDataInterface| null>(null)
        const accessToken = useSelector(
            (state: StateModel) => state.auth.accessToken
        )
        const handleFetchLoadTSData = (id: number) => {
            axios.get(
                `/report/${id}/load/base?resolution=60`,
                { headers: { 'Authorization': 'Bearer ' + accessToken } }
            ).then((response) => {
                setBaseLoad(response.data)
            }).catch((error) => {
                if (error.response.status === 401) {
                    localStorage.removeItem('state')
                }
            })
        }


        useEffect(()=> {
            handleFetchLoadTSData(4)
        }, [])
        return (<div className="w-full">
        
            {
                baseLoad && baseLoad.data.length > 0 &&
                <Plot
                    data={[
                    {
                        x: getDateTimeList(baseLoad.start_date, 
                            baseLoad.resolution,
                            baseLoad.data.length),
                        y: baseLoad.data,
                        type: 'scatter',
                        mode: 'lines+markers',
                        marker: {color: 'red'},
                    },
                    ]}
                    layout={ { title: 'Timeseries data plot'} }
                    className="w-full"
                />
            }
            
        </div>);
}