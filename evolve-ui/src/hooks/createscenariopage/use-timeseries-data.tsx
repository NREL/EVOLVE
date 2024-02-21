import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { StateModel } from '../../interfaces/redux-state';
import { useSelector } from 'react-redux';
import { TimeSeriesDataInfoModel } from '../../interfaces/data-manage-interfaces';

const UseTimeseriesData = ():
    [TimeSeriesDataInfoModel[], React.Dispatch<React.SetStateAction<TimeSeriesDataInfoModel[]>>] => {

    const [allTSdata, setallTSdata] = useState<TimeSeriesDataInfoModel[]>([])
    const accessToken = useSelector((state: StateModel) => state.auth.accessToken)

    useEffect(() => {
        axios.get(
            `/data`,
            { headers: { 'Authorization': 'Bearer ' + accessToken } }
        ).then((response) => {
            setallTSdata(response.data)
        }).catch((error) => {
            console.log(error)
            if (error.response.status === 401) {
                localStorage.removeItem('state')
            }
        })
    }, [])

    return [allTSdata, setallTSdata]

}

export { UseTimeseriesData }