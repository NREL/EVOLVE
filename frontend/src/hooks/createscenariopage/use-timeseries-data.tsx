import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {StateModel} from '../../interfaces/redux-state';
import {useSelector} from 'react-redux';

const UseTimeseriesData = () => {

    const [allTSdata, setallTSdata] = useState<Record<string, any>>([])
    const accessToken = useSelector((state:StateModel) => state.auth.accessToken)
    
    useEffect(()=> {  
        axios.get(
            `/data`,
            {headers: {'Authorization': 'Bearer ' + accessToken}}
        ).then((response)=> {
            setallTSdata(response.data)
        }).catch((error)=> {
            console.log(error)
            if (error.response.status === 401) {
                localStorage.removeItem('state')
            }
        })
    }, [])

    return [allTSdata, setallTSdata]

}

export {UseTimeseriesData}