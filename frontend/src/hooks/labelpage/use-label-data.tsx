import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useSelector } from 'react-redux';
import { StateModel } from "../../interfaces/redux-state";
import {LabelDataInterface} from '../../interfaces/label-interfaces';

const useLabelData = (): [
    LabelDataInterface[], 
    boolean, 
    React.Dispatch<React.SetStateAction<number>>,
    (id: number) => void
] => {

    const [labelData, setLabelData] = useState<LabelDataInterface[]>([])
    const [isLoading, setIsLoading] = useState(false)
    const [reload, setReload] = useState(0)

    const accessToken = useSelector(
        (state: StateModel) => state.auth.accessToken
    )

    const handleDeleteLabel = (id: number) => {
        axios.delete(
            `/label/${id}`,
            { headers: { 'Authorization': 'Bearer ' + accessToken } }
        ).then((response) => {
            console.log(response.data)
            setReload((value:number)=> value + 1)
        }).catch((error) => {
            if (error.response.status === 401) {
                localStorage.removeItem('state')
            }
        })
    }

    const fetchLabels = () => {
        setIsLoading(true)
        axios.get(
            '/label',
            { headers: { 'Authorization': 'Bearer ' + accessToken } }
        ).then((response) => {
            setLabelData(response.data)
            setIsLoading(false)
        }).catch((error) => {
            if (error.response.status === 401) {
                localStorage.removeItem('state')
            }
            setIsLoading(false)
        })
    }

    // reload use effect
    useEffect(() => {
        fetchLabels()
    }, [reload])

    // fetch the data from API    
    useEffect(() => {
        fetchLabels()
    }, [])

    return [labelData, isLoading, setReload, handleDeleteLabel];

}

export { useLabelData };