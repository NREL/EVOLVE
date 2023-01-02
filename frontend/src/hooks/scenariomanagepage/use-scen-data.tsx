import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useSelector } from 'react-redux';
import { StateModel } from "../../interfaces/redux-state";
import { ScenarioDataInterface } from '../../interfaces/scenario-data-interfaces';

const useScenarioData = (): [
    ScenarioDataInterface[], boolean, React.Dispatch<React.SetStateAction<number>>
] => {

    const [scenarioData, setScenarioData] = useState<ScenarioDataInterface[]>([])
    const [isLoading, setIsLoading] = useState(false)
    const [reload, setReload] = useState(0)

    const accessToken = useSelector(
        (state: StateModel) => state.auth.accessToken
    )

    const fetchScenarios = () => {
        setIsLoading(true)
        axios.get(
            '/scenario',
            { headers: { 'Authorization': 'Bearer ' + accessToken } }
        ).then((response) => {
            setScenarioData(response.data)
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
        fetchScenarios()
    }, [reload])

    // fetch the data from API    
    useEffect(() => {
        fetchScenarios()
    }, [])

    return [scenarioData, isLoading, setReload];

}

export { useScenarioData };