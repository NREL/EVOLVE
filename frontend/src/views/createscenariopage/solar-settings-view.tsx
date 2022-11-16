import React, {useState } from 'react';
import { TextField } from '../../components/text-field';
import { SearchDataView } from './search-data-view';
import {useDebouncedSearch} from '../../hooks/use-debounced-search-create-scenarios';

export function SolarSettingsView (props:any) {
    const {formData, handleChange, errors,
        allTSdata, selectedIrrProfile, setSelectedIrrProfile, handleSolarDelete} = props;
    
    const [searchProfiles, setSearchProfiles] = useState<Record<string, any>>([])
    const [isClicked, setIsClicked] = useState(false)
    const [collpased, setCollapsed] = useState(false)

    const irrProfileExist = allTSdata.filter((d:any)=> d.category=== 'irradiance')
    
    useDebouncedSearch(
        allTSdata,
        formData.irradianceData,
        'irradiance',
        setSearchProfiles
    )

    return (
        <React.Fragment>
            <div className="bg-gray-300 w-full my-5 pb-5">
                <div className="bg-blue-500 h-8 flex items-center justify-between px-2">
                    <div className="flex">
                        <img src="./images/solar_icon.svg" width="25"/>
                        <p className="text-white pl-2"> {formData.name} </p>
                        <p className="w-6 h-6 bg-blue-800 text-white flex items-center 
                            justify-center pb-1 ml-5 rounded-full hover:bg-blue-600 hover:cursor-pointer"
                            onClick={()=> handleSolarDelete(formData.id)}
                        > x </p>
                    </div>
                    <div 
                    className="hover:cursor-pointer"
                    onClick={()=> setCollapsed( value=> !value)}
                    >
                        {collpased ? <img src="./images/collapse.svg"/> : <img src="./images/uncollapse.svg"/>}
                    </div>
                </div>
                    
                {
                    !collpased && <React.Fragment>
                    <div className="grid grid-cols-2 md:grid-cols-3 mx-10 my-3 gap-y-2 gap-x-5">

                        <div>
                            <p> Capacity (kW) </p>
                            <p className='text-sm text-gray-500 pb-2'> Enter total solar capacity in kW. </p>
                            <TextField 
                                    error={errors.solarCapacity}
                                    name="solarCapacity"
                                    type="number"
                                    value={formData.solarCapacity}
                                    onChange={handleChange}
                                />
                        </div>
                        
                        <div>
                            <p> Irradiance data </p>
                            <p className='text-sm text-gray-500 pb-2'> Search for solar profile and select one.
                            {
                                    irrProfileExist.length === 0 && <span className="text-red-500 pl-1 ">
                                        Note Load profile does not exist yet consider uploading data first.
                                    </span>
                                }
                            </p>
                            {
                            !isClicked ? <TextField 
                                error={errors.irradianceData}
                                name="irradianceData"
                                type="text"
                                value={formData.irradianceData}
                                onChange={handleChange}
                                />: <div className="flex py-1">
                                        <p> {selectedIrrProfile.name} <span className="bg-blue-500 px-1 rounded-md 
                                        text-white text-sm text-center"> {selectedIrrProfile.owner} </span> 
                                        </p>  
                                        <p className="ml-3 bg-gray-200 text-center w-6 h-6 rounded-full text-sm 
                                        items-center flex justify-center hover:bg-gray-400 hover:cursor-pointer"
                                        onClick={()=> {
                                            setIsClicked(false)
                                            setSelectedIrrProfile({})
                                        }}
                                        > X </p>
                                </div>
                            }
                            
                            {searchProfiles.length >0 && !isClicked && <SearchDataView
                                searchProfiles={searchProfiles}
                                setSelectedProfile={setSelectedIrrProfile}
                                setIsClicked={setIsClicked}
                                setSearchProfiles={setSearchProfiles}
                            />
                            }
                        </div>

                        

                    </div>


                    <div className="flex items-center mt-5 mx-10">
                                <p className="pr-2"> Solar installation type </p>
                                <select className="rounded-md h-8 w-40 px-2" name="solarInstallationStrategy" 
                                    value={formData.solarInstallationStrategy} 
                                    onChange={handleChange}
                                >
                                    <option value="fixed">Fixed installation</option>
                                    <option value="single_axis">Single Axis Tracking</option>
                                    <option value="dual_axis">Dual Axis Tracking</option>
                                </select>
                    </div>


                    <div className="grid grid-cols-2 md:grid-cols-3 mx-10 my-3 gap-y-2 gap-x-5">
                        
                        
                        { formData.solarInstallationStrategy !== 'dual_axis' &&
                            <div>
                                <p> Azimuth (degrees) </p>
                                <p className='text-sm text-gray-500 pb-2'> Angle solar panel is facing measured in clockwise 
                                direction from North. </p>
                                <TextField 
                                    error={errors.panelAzimuth}
                                    name="panelAzimuth"
                                    type="number"
                                    value={formData.panelAzimuth}
                                    onChange={handleChange}
                                />
                            </div>
                        }

                        {
                            formData.solarInstallationStrategy === 'fixed' && <div>
                                <p> Tilt (degrees) </p>
                                <p className='text-sm text-gray-500 pb-2'> Angle the panel is tilted from the horizontal ground earth surface. 
                                </p>
                                <TextField 
                                    error={errors.panelTilt}
                                    name="panelTilt"
                                    type="number"
                                    value={formData.panelTilt}
                                    onChange={handleChange}
                                />
                            </div>
                        }

                            <div>
                                <p> DC/AC ratio </p>
                                <p className='text-sm text-gray-500 pb-2'> DC AC ratio is used to compute inverter output. Value greater than 1 would 
                                not saturate output.
                                </p>
                                <TextField 
                                    error={errors.dcacRatio}
                                    name="dcacRatio"
                                    type="number"
                                    value={formData.dcacRatio}
                                    onChange={handleChange}
                                />
                            </div>
                    </div>
                </React.Fragment>
                }
            </div>
        </React.Fragment>
    )
}