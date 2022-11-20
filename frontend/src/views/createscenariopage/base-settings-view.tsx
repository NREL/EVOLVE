import React, { useEffect, useState } from 'react';
import { TextField } from '../../components/text-field';
import { debounce } from "lodash";
import { SearchDataView } from './search-data-view';
import { useDebouncedSearch } from '../../hooks/use-debounced-search-create-scenarios';


export function BaseSettingsView(props: any) {
    const { formData, handleChange, errors, allTSdata,
        selectedProfile, setSelectedProfile, dateRange, fillData } = props;
    const [searchProfiles, setSearchProfiles] = useState<Record<string, any>>([])
    const [isClicked, setIsClicked] = useState(false)

    const loadProfileExist = allTSdata.filter((d: any) => d.category === 'kW')

    useDebouncedSearch(
        allTSdata,
        formData.loadProfile,
        'kW',
        setSearchProfiles
    )


    return (
        <React.Fragment>
            <div className="bg-gray-300 w-full my-10 pb-5">
                <div className="bg-blue-500 h-8 flex items-center px-2">
                    <img src="./images/solar_icon.svg" width="25" />
                    <p className="text-white pl-2"> Basic settings </p>
                </div>

                <div className="grid grid-cols-2 md:grid-cols-3 mx-10 my-3 gap-y-2 gap-x-5">

                    <div className='relative'>
                        <p> Load profile </p>

                        <p className='text-sm text-gray-500 pb-2'> Search for a profle and select one.
                            {
                                loadProfileExist.length === 0 && <span className="text-red-500 pl-1 ">
                                    Note Load profile does not exist yet consider uploading data first.
                                </span>
                            }
                        </p>

                        {!isClicked ? <TextField
                            error={errors.loadProfile}
                            name="loadProfile"
                            value={formData.loadProfile}
                            onChange={handleChange}
                        /> :
                            <div className="flex py-1">
                                <p> {selectedProfile.name} <span className="bg-blue-500 px-1 rounded-md 
                                text-white text-sm text-center"> {selectedProfile.owner} </span>
                                </p>
                                <p className="ml-3 bg-gray-200 text-center w-6 h-6 rounded-full text-sm 
                                items-center flex justify-center hover:bg-gray-400 hover:cursor-pointer"
                                    onClick={() => {
                                        setIsClicked(false)
                                        setSelectedProfile({})
                                    }}
                                > X </p>
                            </div>
                        }

                        {searchProfiles.length > 0 && !isClicked && <SearchDataView
                            searchProfiles={searchProfiles}
                            setSelectedProfile={setSelectedProfile}
                            setIsClicked={setIsClicked}
                            setSearchProfiles={setSearchProfiles}
                        />
                        }


                    </div>

                    <div>
                        <p> Start date </p>
                        <p className='text-sm text-gray-500 pb-2'> Allowed date range is {dateRange.min} - {dateRange.max}</p>
                        <TextField
                            error={errors.startDate}
                            name="startDate"
                            type="date"
                            value={formData.startDate}
                            onChange={handleChange}
                            min={dateRange.min}
                            max={dateRange.max}
                        />
                    </div>

                    <div>
                        <p> End date </p>
                        <p className='text-sm text-gray-500 pb-2'> Allowed date range is {dateRange.min} - {dateRange.max}</p>
                        <TextField
                            error={errors.endDate}
                            name="endDate"
                            type="date"
                            value={formData.endDate}
                            onChange={handleChange}
                            min={dateRange.min}
                            max={dateRange.max}
                        />
                    </div>

                    <div>
                        <p> Data resolution </p>
                        <p className='text-sm text-gray-500 pb-2'> Choose data resolution in minute. </p>
                        <TextField
                            error={errors.resolution}
                            name="resolution"
                            type="number"
                            value={formData.resolution}
                            onChange={handleChange}
                        />
                    </div>

                    {
                        fillData && <div>
                            <p> Strategy for data filling </p>
                            <p className='text-sm text-gray-500 pb-2'> Choose a strategy to fll missing data point. </p>
                            <select className="rounded-md h-8 w-40 px-2" name="dataFillingStrategy" value={formData.dataFillingStrategy} onChange={handleChange}>
                                <option value="interpolation">Linear interpolation</option>
                                <option value="staircase">Staircase fill</option>
                            </select>
                        </div>
                    }

                </div>
            </div>
        </React.Fragment>
    )
}