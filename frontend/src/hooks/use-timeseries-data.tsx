// Managing time series data cards

import {TimeSeriesDataInfoModel} from "../interfaces/data-manage-interfaces";
import {StateModel} from "../interfaces/redux-state";
import { useState, useEffect } from "react";
import axios from 'axios';
import {useSelector} from 'react-redux';

const useTimeSeriesData = (reload: number) => {

    const [timeseriesData, setTimeseriesData] = useState<TimeSeriesDataInfoModel[]>([])
    const [timeseriesDataBackup, setTimeseriesDataBackup] = useState<TimeSeriesDataInfoModel[]>([])
    const [isLoading, setIsLoading] = useState(true)
    const accessToken = useSelector(
        (state:StateModel) => state.auth.accessToken
    )

    useEffect(()=> {
        axios.get(
            '/data',
            {headers: {'Authorization': 'Bearer ' + accessToken}}
        ).then((response)=> {

            let timeseriesData = response.data
            setTimeseriesDataBackup(timeseriesData)
            setTimeseriesData(timeseriesData.sort((
                a: TimeSeriesDataInfoModel,
                b: TimeSeriesDataInfoModel
            )=> {
                return  new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
            }))
            setIsLoading(false)

        }).catch((error)=> {
            
            if (axios.isCancel(error)){
                console.log("cancelled!")
            }
            if (error.response.status === 401) {
                localStorage.removeItem('state')
            }
            setIsLoading(false)
        })
    }, [reload])

    return [timeseriesData, timeseriesDataBackup, 
        isLoading, setTimeseriesData]
}

export {useTimeSeriesData}