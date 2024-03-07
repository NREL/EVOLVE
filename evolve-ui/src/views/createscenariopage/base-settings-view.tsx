import React, { useState } from 'react';
import { TextField } from '../../components/text-field';
import {HiOutlineInformationCircle} from 'react-icons/hi';
import { SearchDataView } from './search-data-view';
import { useDebouncedSearch } from '../../hooks/use-debounced-search-create-scenarios';
import { DataFilingStrategyDesc } from './descriptions/load-filling-strategy-desc';
import { ColoredHeaderSection } from './header-section';


export function BaseSettingsView(props: any) {
    const { formData, handleChange, errors, allTSdata,
        selectedProfile, setSelectedProfile, dateRange, fillData, updateFlag } = props;
    
    const [searchProfiles, setSearchProfiles] = useState<Record<string, any>[]>([])
    const [isClicked, setIsClicked] = useState(updateFlag);
    const [closeDesView, setCloseDesView] = useState(true);
    const [descriptionComp, setDescriptionComp] = useState<any>(null);
    const loadProfileExist = allTSdata.filter((d: any) => d.category === 'kW');

    useDebouncedSearch(
        allTSdata,
        formData.loadProfile,
        'kW',
        setSearchProfiles
    )


    return (
        <React.Fragment>
            {!closeDesView && descriptionComp}
            <div className="bg-gray-300 w-full my-10 pb-5">
                
                <ColoredHeaderSection 
                    title='Simulation Settings'
                    description='Select load profile, simulation time as well as 
                    resolution for the simulation.'
                    image='./images/timeseries_data.svg'
                />

                <div className="grid grid-cols-2 md:grid-cols-3 mx-10 my-3 gap-y-2 gap-x-5">

                    <div className='relative'>
                        <p> Load Profile </p>

                        <p className='text-sm text-gray-500 pb-2'> Select a load profile by typing name.
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
                                <p> {selectedProfile && selectedProfile.name} <span className="bg-blue-500 px-1 rounded-md 
                                    text-white text-sm text-center"> {selectedProfile && selectedProfile.owner} </span>
                                </p>
                                <p className="ml-3 bg-gray-200 text-center w-6 h-6 rounded-full text-sm 
                                    items-center flex justify-center hover:bg-gray-400 hover:cursor-pointer"
                                    onClick={() => {
                                        setIsClicked(false)
                                        setSelectedProfile(null)
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
                        <p> Start Date </p>
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
                        <p> End Date </p>
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
                        <p> Time Resolution </p>
                        <p className='text-sm text-gray-500 pb-2'> Input time resolution for analysis (minutes). Note if time resolution does not match data 
                        you selected you would have to also select appropriate interpolation method. </p>
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
                            <div className='flex gap-x-3 items-center'>
                                <p> Strategy for data filling </p>
                                <HiOutlineInformationCircle size={20} 
                                    className='text-gray-500 hover:text-blue-500 hover:cursor-pointer'
                                    onClick={()=> {
                                        setCloseDesView(false)
                                        setDescriptionComp(
                                            <DataFilingStrategyDesc setCloseView={setCloseDesView}/>
                                        )}}
                                /> 
                            </div>
                            
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