import React, { useState } from 'react';
import { TextField } from '../../components/text-field';
import { SelectField } from '../../components/select-field';
import { SearchDataView } from './search-data-view';
import { useDebouncedSearch } from '../../hooks/use-debounced-search-create-scenarios';


export function ESSettingsView(props: any) {
    const { formData, handleChange, errors,
        allTSdata, selectedPriceProfile, setSelectedPriceProfile,
        handleEnergyStorageDelete, updateFlag } = props;

    const [searchProfiles, setSearchProfiles] = useState<Record<string, any>>([])
    const [isClicked, setIsClicked] = useState(updateFlag)
    const [collpased, setCollapsed] = useState(false)

    const hours = ['12 AM', '1 AM', '2 AM', '3 AM', '4 AM', '5 AM',
        '6 AM', '7 AM', '8 AM', '9 AM', '10 AM', '11 AM', '12 PM',
        '1 PM', '2 PM', '3 PM', '4 PM', '5 PM', '6 PM', '7 PM',
        '8 PM', '9 PM', '10 PM', '11 PM']

    const priceProfileExist = allTSdata.filter((d: any) => d.category === 'price')

    useDebouncedSearch(
        allTSdata,
        formData.priceProfile,
        'price',
        setSearchProfiles
    )

    return (
        <React.Fragment>
            <div className="bg-gray-300 w-full my-10 pb-5">
                <div className="bg-blue-500 h-8 flex items-center justify-between px-2">
                    <div className="flex">
                        <img src="./images/ev_icon.svg" width="25" />
                        <p className="text-white pl-2"> {formData.name} </p>
                        <p className="w-6 h-6 bg-blue-800 text-white flex items-center 
                                justify-center pb-1 ml-5 rounded-full hover:bg-blue-600 hover:cursor-pointer"
                            onClick={() => handleEnergyStorageDelete(formData.id)}
                        > x </p>
                    </div>
                    <div
                        className="hover:cursor-pointer"
                        onClick={() => setCollapsed(value => !value)}
                    >
                        {collpased ? <img src="./images/collapse.svg" /> : <img src="./images/uncollapse.svg" />}
                    </div>
                </div>

                {
                    !collpased && <React.Fragment>

                        <div className="mx-10 my-3">


                            <div className="grid grid-cols-2 md:grid-cols-3 gap-y-2 mt-3 gap-x-5">

                                {
                                    !formData.isESOptimal && <React.Fragment>

                                        <div>
                                            <p> Maximum Power Capacity (kW) </p>
                                            <p className='text-sm text-gray-500 pb-2'>
                                                Battery power capacity in kW </p>
                                            <TextField
                                                error={errors?.esPowerCapacity}
                                                name="esPowerCapacity"
                                                type="number"
                                                value={formData.esPowerCapacity}
                                                onChange={handleChange}
                                            />
                                        </div>

                                        <div>
                                            <p> Energy Capacity (kWh) </p>
                                            <p className='text-sm text-gray-500 pb-2'>
                                                Battery energy capacity in kW </p>
                                            <TextField
                                                error={errors?.esEnergyCapacity}
                                                name="esEnergyCapacity"
                                                type="number"
                                                value={formData.esEnergyCapacity}
                                                onChange={handleChange}
                                            />
                                        </div>
                                    </React.Fragment>
                                }

                            </div>

                            <div className="flex items-center mt-5">
                                <p className="pr-2"> Charging/Discharging Strategy </p>
                                <select className="rounded-md h-8 w-32 px-2" name="esStrategy" value={formData.esStrategy} onChange={handleChange}>
                                    <option value="time">Time Based</option>
                                    {/* <option value="price">Price Based</option> */}
                                    <option value="self_consumption">Self consumption</option>
                                    <option value="peak_shaving">Peak shaving</option>
                                </select>
                            </div>
                            <p className='text-sm text-gray-500 pb-2'>
                                Pick a strategy to be used for charging and discharging a battery. </p>
                            {
                                formData.esStrategy === 'time' && <div className="mt-3">

                                    <div>
                                        <p> Charging hours </p>
                                        <p className='text-sm text-gray-500 pb-2'>
                                            Set charging hours for battery. </p>
                                        <div className="grid grid-cols-12 gap-y-3 py-2">
                                            {
                                                hours.map((hour) => {
                                                    return (<div className="flex items-center pr-2">
                                                        <SelectField
                                                            name="chargingHours"
                                                            value={hour}
                                                            onChange={handleChange}
                                                            checked={formData.chargingHours.includes(hour)}
                                                            disabled={formData.disChargingHours.includes(hour)}
                                                        />
                                                        <p className="pl-2"> {hour} </p>
                                                    </div>)
                                                })
                                            }
                                        </div>
                                    </div>

                                    <div>
                                        <p> Discharging hours </p>
                                        <p className='text-sm text-gray-500 pb-2'>
                                            Set discharging hours for battery. </p>
                                        <div className="grid grid-cols-12 gap-y-3 py-2">
                                            {
                                                hours.map((hour) => {
                                                    return (<div className="flex items-center pr-2">
                                                        <SelectField
                                                            name="disChargingHours"
                                                            value={hour}
                                                            onChange={handleChange}
                                                            checked={formData.disChargingHours.includes(hour)}
                                                            disabled={formData.chargingHours.includes(hour)}
                                                        />
                                                        <p className="pl-2"> {hour} </p>
                                                    </div>)
                                                })
                                            }
                                        </div>
                                    </div>
                                </div>
                            }

                            {
                                formData.esStrategy === 'price' && <div className="grid gap-x-5 grid-cols-2 md:grid-cols-3 gap-y-2 mt-3">

                                    <div>
                                        <p> Price profile </p>
                                        <p className='text-sm text-gray-500 pb-2'>
                                            Search for price profile and select.
                                            {
                                                priceProfileExist.length === 0 && <span className="text-red-500 pl-1 ">
                                                    Note price profile does not exist yet consider uploading data first.
                                                </span>
                                            }
                                        </p>
                                        {
                                            !isClicked ? <TextField
                                                error={errors.priceProfile}
                                                name="priceProfile"
                                                value={formData.priceProfile}
                                                onChange={handleChange}
                                            /> : <div className="flex py-1">
                                                <p> {selectedPriceProfile.name} <span className="bg-blue-500 px-1 rounded-md 
                                                                            text-white text-sm text-center"> {selectedPriceProfile.owner} </span>
                                                </p>
                                                <p className="ml-3 bg-gray-200 text-center w-6 h-6 rounded-full text-sm 
                                                                            items-center flex justify-center hover:bg-gray-400 hover:cursor-pointer"
                                                    onClick={() => {
                                                        setIsClicked(false)
                                                        setSelectedPriceProfile({})
                                                    }}
                                                > X </p>
                                            </div>
                                        }

                                        {searchProfiles.length > 0 && !isClicked && <SearchDataView
                                            searchProfiles={searchProfiles}
                                            setSelectedProfile={setSelectedPriceProfile}
                                            setIsClicked={setIsClicked}
                                            setSearchProfiles={setSearchProfiles}
                                        />
                                        }


                                    </div>

                                    <div>
                                        <p> Price threshold for charging ($) </p>
                                        <p className='text-sm text-gray-500 pb-2'>
                                            Price below which to charge the battery. </p>
                                        <TextField
                                            error={errors.chargingPrice}
                                            name="chargingPrice"
                                            type="number"
                                            value={formData.chargingPrice}
                                            onChange={handleChange}
                                        />
                                    </div>

                                    <div>
                                        <p>  Price threshold for discharging ($) </p>
                                        <p className='text-sm text-gray-500 pb-2'>
                                            Price above which to discharge the battery. </p>
                                        <TextField
                                            error={errors.disChargingPrice}
                                            name="disChargingPrice"
                                            type="number"
                                            value={formData.disChargingPrice}
                                            onChange={handleChange}
                                        />
                                    </div>
                                </div>
                            }

                            {
                                formData.esStrategy === 'peak_shaving' && <div className="grid gap-x-5 grid-cols-2 md:grid-cols-3 gap-y-2 mt-3">

                                    <div>
                                        <p> Power threshold for charging (% of peak power) </p>
                                        <p className='text-sm text-gray-500 pb-2'>
                                            When load drops below this power battery starts to charge until fully charged. </p>
                                        <TextField
                                            error={errors?.chargingPowerThreshold}
                                            name="chargingPowerThreshold"
                                            type="number"
                                            value={formData.chargingPowerThreshold}
                                            onChange={handleChange}
                                        />
                                    </div>

                                    <div>
                                        <p>  Power threshold for discharging (% of peak power) </p>
                                        <p className='text-sm text-gray-500 pb-2'>
                                            When load increases below this power battery starts to charge until fully discharged. </p>
                                        <TextField
                                            error={errors?.dischargingPowerThreshold}
                                            name="dischargingPowerThreshold"
                                            type="number"
                                            value={formData.dischargingPowerThreshold}
                                            onChange={handleChange}
                                        />
                                    </div>
                                </div>
                            }


                        </div>


                    </React.Fragment>
                }

            </div>
        </React.Fragment>
    )
}