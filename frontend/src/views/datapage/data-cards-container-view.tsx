import React from 'react';
import {DataFilterCard} from './data-card-filter-view';
import {DataCards} from './data-cards-view';
import {IsCardDataLoading} from './is-data-card-loading';
import { TimeSeriesDataInfoModel } from '../../interfaces/data-manage-interfaces';

export function DataCardsContainer(props:any) {

    
    const {setcardData, isClicked, setIsClicked, timeseriesData,
        setTimeseriesData, timeseriesDataBackup,
        filterHover, setFilterHover, isLoading, kWCheck,
        setkWCheck, irrCheck, setIrrCheck, sortDate, setSortDate, 
        navigation} = props


    
    const handleSearch = (e: any) => {
        setTimeseriesData(
            timeseriesDataBackup.filter( 
                (el:TimeSeriesDataInfoModel)=> el.name.search(e.target.value) !== -1
            )
        )
    }

    
    return (
        <div className="mb-5 relative px-10">
            
            <div className="flex mt-5">
                <div className="flex bg-[#e9e9e9] w-full rounded-md">
                    <img src="./images/search.svg" className="pl-3 py-1" width="22"/>
                    <input 
                        placeholder="Search by name" 
                        className="px-3 py-1 bg-[#e9e9e9] outline-0 border-0 w-full"
                        name="search"
                        onChange={(e: any)=> handleSearch(e)}
                        />
                </div>
                <button 
                    className="bg-blue-500 text-white py-1 px-3 rounded-md ml-3"
                    onMouseOver={()=> setFilterHover(true)}
                    onMouseLeave={()=> setFilterHover(false)}
                    > 
                    Filter 
                </button>
            </div>

            { filterHover ? 
                    <div 
                        className="absolute right-0 top-5 right-5 px-3 py-3 
                        bg-gray-100 w-1/4 shadow-md z-25 hover:cursor-pointer"
                        onMouseOver={()=> setFilterHover(true)}
                        onMouseLeave={()=> setFilterHover(false)}
                    >
                    <DataFilterCard 
                        kWFilterValue={kWCheck}
                        irrFilterValue={irrCheck}
                        sortDateValue={sortDate}
                        setkWFilterValue={setkWCheck}
                        setirrFilterValue={setIrrCheck}
                        setSortDateValue={setSortDate}
                    />
                    </div> : null
            }

            <div className="flex justify-center bg-blue-500 w-full sm:w-60 h-10 rounded-md m-auto mt-5" 
                onClick={()=> {navigation('/data/upload')}}>
                <button type="button" className="text-xl text-white font-bold pr-3"> Upload data </button>
                <img src="./images/upload_white_logo.svg" className="w-12"/> 
            </div>

            <div className="flex justify-between my-5">
                <h1 className="text-xl text-blue-500 font-bold"> My Timeseries Data </h1>
            </div>

            {
                isLoading ? 
                    <IsCardDataLoading/> :
                    <div>
                        <DataCards 
                            data={timeseriesData}
                            isClicked={isClicked} 
                            setcardData={setcardData}
                            setIsClicked={setIsClicked}
                            />
                    </div>
            }

        </div>
    )
}
