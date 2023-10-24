// Managing time series data cards

import { TimeSeriesDataCategory, 
    DateSortString} from "../interfaces/data-manage-interfaces";
import {TimeSeriesDataInfoModel} from "../interfaces/data-manage-interfaces";
import {  useEffect } from "react";


const useFilterTimeSeriesData = (
    kWCheck: boolean,
    irrCheck: boolean,
    sortDate: DateSortString,
    reload: number,
    timeseriesDataBackup:any,
    setTimeseriesData: any
) => {

    useEffect(()=> {
        
        let sortedTimeseriesData = []
        if (sortDate === DateSortString.descending){
            sortedTimeseriesData = timeseriesDataBackup.sort(
                (
                    a: TimeSeriesDataInfoModel,
                    b: TimeSeriesDataInfoModel
                ) => {
                    return new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
                }
            )
        } else {
            sortedTimeseriesData = timeseriesDataBackup.sort(
                (
                    a: TimeSeriesDataInfoModel,
                    b: TimeSeriesDataInfoModel
                ) => {
                    return new Date(a.created_at).getTime() - new Date(b.created_at).getTime()
                }
            )
        }
        setTimeseriesData(
            sortedTimeseriesData.filter( (el:TimeSeriesDataInfoModel) => {
                return (el.category === TimeSeriesDataCategory.kW && kWCheck) ||
                (el.category === TimeSeriesDataCategory.irradiance && irrCheck)
            })
        )

    }, [kWCheck, irrCheck, sortDate, timeseriesDataBackup, reload])

}

export {useFilterTimeSeriesData}