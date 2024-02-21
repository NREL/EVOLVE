import React, { useState, useEffect }  from 'react';
import { ScenarioDataInterface } from '../../interfaces/scenario-data-interfaces';
import { ReportDataInterface } from '../../interfaces/report-interfaces';
import axios from 'axios';
import { useSelector } from 'react-redux';
import { StateModel } from "../../interfaces/redux-state";


const useReportData = (isClicked: ScenarioDataInterface | null): [
    ReportDataInterface[], (value: number) => void
] => {
    const [reportData, setReportData] = useState<ReportDataInterface[]>([])
    const accessToken = useSelector(
        (state: StateModel) => state.auth.accessToken
    )
    
    const handleFetchReports = (id: number) => {
        axios.get(
            `/scenario/${id}/report`,
            { headers: { 'Authorization': 'Bearer ' + accessToken } }
        ).then((response) => {
            setReportData(response.data)
        }).catch((error) => {
            if (error.response.status === 401) {
                localStorage.removeItem('state')
            }
        })
    }

    useEffect(() => {
        isClicked && handleFetchReports(isClicked.id)
    }, [isClicked])

    return [reportData, handleFetchReports]
}

export {useReportData};