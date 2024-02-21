import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useSelector } from 'react-redux';
import { StateModel } from "../../interfaces/redux-state";
import { ScenarioDataInterface } from "../../interfaces/scenario-data-interfaces";

const useScenarioJSON = (isClicked: ScenarioDataInterface | null): [
    any, (value: number) => void
] => {

    const [scenJSON, setScenJSON] = useState({})
    const accessToken = useSelector(
        (state: StateModel) => state.auth.accessToken
    )

    const handleFetchJSON = (id: number) => {
        axios.get(
            `/scenario/${id}`,
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
        isClicked && handleFetchJSON(isClicked.id)
    }, [isClicked])

    return [scenJSON, handleFetchJSON];
}

export { useScenarioJSON };