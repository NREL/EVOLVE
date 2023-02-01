import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useSelector } from 'react-redux';
import { StateModel } from "../../interfaces/redux-state";

const useScenDataFromId = (scen_id: any): [
    any, (value: number) => void
] => {

    const [scenJSON, setScenJSON] = useState({})
    const accessToken = useSelector(
        (state: StateModel) => state.auth.accessToken
    )

    const handleFetchJSON = (id: number) => {
        axios.get(
            `/report/scenjson/${id}`,
            { headers: { 'Authorization': 'Bearer ' + accessToken } }
        ).then((response) => {
            setScenJSON(response.data)

        }).catch((error) => {
            if (error.response.status === 401) {
                localStorage.removeItem('state')
            }
        })
    }

    useEffect(() => {
        scen_id && handleFetchJSON(scen_id)
    }, [])

    return [scenJSON, handleFetchJSON];
}

export { useScenDataFromId };