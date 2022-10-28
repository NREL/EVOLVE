import React from 'react';
import { useState, useEffect } from "react";
import axios from 'axios';
import {useSelector} from 'react-redux';
import DataCardDetail from "./data-card-detail-controller";
import {DataCardsContainer} from "./data-cards-container-view";
import {DateSortString} from "../../interfaces/data-manage-interfaces";
import {TimeSeriesDataInfoModel} from "../../interfaces/data-manage-interfaces";
import {StateModel} from "../../interfaces/redux-state";
import {useTimeSeriesData,
    useFilterTimeSeriesData,
    useTimeseriesDataComments} from "../../hooks";
    import { useNavigate} from "react-router-dom";


function DataPage() {
    
    const [timeseriesData, timeseriesDataBackup, 
        isLoading, setTimeseriesData] = useTimeSeriesData()
    
    const navigation = useNavigate();

    const defaultCardData = {
        id: 0,
        name: 'dummy',
        description: 'dummy',
        created_at: Date.now().toString(),
        start_date: Date.now().toString(),
        end_date: Date.now().toString(),
        resolution_min: 0,
        category: null
    }

    const [cardData, setcardData] = useState<TimeSeriesDataInfoModel>(defaultCardData)
    const [isClicked, setIsClicked] = useState(false)
    const [reload, setReload] = useState(0)
    const [filterHover, setFilterHover] = useState(false)
    const [kWCheck, setkWCheck] = useState(true)
    const [irrCheck, setIrrCheck] = useState(true)
    const [sortDate, setSortDate] = useState<DateSortString>(DateSortString.descending)
    
    const accessToken = useSelector( (state: StateModel) => state.auth.accessToken)

    useFilterTimeSeriesData(
        kWCheck, 
        irrCheck, 
        sortDate, 
        reload,
        timeseriesDataBackup,
        setTimeseriesData
    )

    const [comments, setComment, handleInsertComment, 
        handleCommentDelete, handleUpdateComment] = useTimeseriesDataComments(cardData)

    
    const handleDeleteData = (
            data: TimeSeriesDataInfoModel
        ) => {
            // First let's delete the data
        
            axios.delete(`/data/${data.id}`,
                {headers: {'Authorization': 'Bearer ' + accessToken}}
            ).then((response)=> {
                console.log("Sucessfully deleted data ", response)
                
                // Disable card clicked view
                setIsClicked(false)
        
                // Reload the API data
                setReload((value)=> value +1 )
        
            }).catch((error)=> {
                console.log('Not successful', error)
                if (error.response.status === 401) {
                    localStorage.removeItem('state')
                }
            })
            
        }
    
    // View for data card container
    const dataCardContainer = <DataCardsContainer
                                setcardData={setcardData}
                                isClicked={isClicked}
                                setIsClicked={setIsClicked} 
                                timeseriesData={timeseriesData}
                                setTimeseriesData={setTimeseriesData}
                                timeseriesDataBackup={timeseriesDataBackup}
                                filterHover={filterHover}
                                setFilterHover={setFilterHover}
                                isLoading={isLoading}
                                kWCheck={kWCheck}
                                setkWCheck={setkWCheck}
                                irrCheck={irrCheck}
                                setIrrCheck={setIrrCheck}
                                sortDate={sortDate}
                                setSortDate={setSortDate}
                                navigation={navigation}
                            />

    return (
        
            isClicked ? 
                <div className="flex justify-between">
                    <div className="h-[calc(100vh-0rem)] overflow-y-scroll w-full">
                        {dataCardContainer}
                    </div>
                    
                    <div className="h-screen overflow-y-scroll bg-white w-80 shadow-md 
                        opacity-98 p-2 z-10 transition duration-150 ease-linear">
                        <DataCardDetail 
                            data={cardData} 
                            setIsClicked={setIsClicked}
                            setcardData={setcardData}
                            handleDeleteData={handleDeleteData}
                            comments={comments}
                            handleInsertComment={handleInsertComment}
                            handleCommentDelete={handleCommentDelete}
                            handleUpdateComment={handleUpdateComment}
                        />
                    </div> 
                </div> : <div>
                    {dataCardContainer}
                </div>
    )
}

export {DataPage}