import React, { useState } from 'react';
import { TextField } from '../../components/text-field';
import { SelectField } from '../../components/select-field';
import { SearchDataView } from './search-data-view';
import { useDebouncedSearch } from '../../hooks/use-debounced-search-create-scenarios';
import { HiOutlineInformationCircle } from 'react-icons/hi';
import { ESStrategyDescView } from './descriptions/storage-strategy-desc';
import { FormGroupsView } from './utils';


function HoursView(props: any) {

    const hours = ['12 AM', '1 AM', '2 AM', '3 AM', '4 AM', '5 AM',
        '6 AM', '7 AM', '8 AM', '9 AM', '10 AM', '11 AM', '12 PM',
        '1 PM', '2 PM', '3 PM', '4 PM', '5 PM', '6 PM', '7 PM',
        '8 PM', '9 PM', '10 PM', '11 PM'];
    return (
        <>
            {
                hours.map((hour) => {
                    return (<div className="flex items-center pr-2">
                        <SelectField
                            name={props.name}
                            value={hour}
                            onChange={props.handleChange}
                            checked={props.checked(hour)}
                            disabled={props.disabled(hour)}
                        />
                        <p className="pl-2"> {hour} </p>
                    </div>)
                })
            }
        </>
    )
}

function TimeFormGroupsView(props: any) {

    const fields = [
        {
            name: 'chargingHours',
            label: 'Charging hours',
            description: 'Set charging hours for battery.',
            checked: (value: string) =>
                props.formData.chargingHours.includes(value),
            disabled: (value: string) =>
                props.formData.disChargingHours.includes(value)
        },
        {
            name: 'disChargingHours',
            label: 'Discharging hours',
            description: 'Set discharging hours for battery.',
            checked: (value: string) =>
                props.formData.disChargingHours.includes(value),
            disabled: (value: string) =>
                props.formData.chargingHours.includes(value)
        }
    ]

    return (
        <div className="mt-3">
            {
                fields.map((item: any) => {
                    return (
                        <div>
                            <p> {item.label} </p>
                            <p className='text-sm text-gray-500 pb-2'>
                                {item.description} </p>
                            <div className="grid grid-cols-12 gap-y-3 py-2">
                                <HoursView
                                    name={item.name}
                                    handleChange={props.handleChange}
                                    checked={item.checked}
                                    disabled={item.disabled}
                                />
                            </div>
                        </div>
                    )
                })
            }
        </div>
    )
};

function PriceGroupsView(props: any) {
    const fields = [
        {
            label: 'Price threshold for charging ($)',
            description: `Price below which to charge the battery.`,
            error: props.errors?.chargingPrice,
            name: "chargingPrice",
            type: "number",
            value: props.formData.chargingPrice,
        },
        {
            label: 'Price threshold for discharging ($)',
            description: `Price above which to discharge the battery.`,
            error: props.errors?.disChargingPrice,
            name: "disChargingPrice",
            type: "number",
            value: props.formData.disChargingPrice,
        },
    ]
    return (
        <>
            <div className="grid gap-x-5 
                    grid-cols-2 md:grid-cols-3 gap-y-2 mt-3">

                <div>
                    <p> Price profile </p>
                    <p className='text-sm text-gray-500 pb-2'>
                        Search for price profile and select.
                        {
                            props.priceProfileExist.length === 0 && <span className="text-red-500 pl-1 ">
                                Note price profile does not exist yet consider uploading data first.
                            </span>
                        }
                    </p>
                    {
                        !props.isClicked ? <TextField
                            error={props.errors.priceProfile}
                            name="priceProfile"
                            value={props.formData.priceProfile}
                            onChange={props.handleChange}
                        /> : <div className="flex py-1">
                            <p> {props.selectedPriceProfile.name} <span className="bg-blue-500 px-1 rounded-md 
                                                        text-white text-sm text-center">
                                {props.selectedPriceProfile.owner} </span>
                            </p>
                            <p className="ml-3 bg-gray-200 text-center w-6 h-6 rounded-full text-sm 
                                                        items-center flex justify-center 
                                            hover:bg-gray-400 hover:cursor-pointer"
                                onClick={() => {
                                    props.setIsClicked(false)
                                    props.setSelectedPriceProfile({})
                                }}
                            > X </p>
                        </div>
                    }

                    {props.searchProfiles.length > 0 && !props.isClicked && <SearchDataView
                        searchProfiles={props.searchProfiles}
                        setSelectedProfile={props.setSelectedPriceProfile}
                        setIsClicked={props.setIsClicked}
                        setSearchProfiles={props.setSearchProfiles}
                    />
                    }


                </div>

                <FormGroupsView
                    formFields={fields}
                    handleChange={props.handleChange}
                />
            </div>
        </>
    )
}

export function ESSettingsView(props: any) {
    const { formData, handleChange, errors,
        allTSdata, selectedPriceProfile, setSelectedPriceProfile,
        handleEnergyStorageDelete, updateFlag } = props;

    const [searchProfiles, setSearchProfiles] = useState<Record<string, any>>([]);
    const [isClicked, setIsClicked] = useState(updateFlag);
    const [collpased, setCollapsed] = useState(false);
    const [descriptionComp, setDescriptionComp] = useState<any>(null)
    const [closeDesView, setCloseDesView] = useState(true)

    const priceProfileExist = allTSdata.filter((d: any) => d.category === 'price');
    const formFields = [
        {
            label: 'Maximum Power Capacity (kW)',
            description: 'Battery power capacity in kW',
            error: errors?.esPowerCapacity,
            name: "esPowerCapacity",
            type: "number",
            value: formData.esPowerCapacity,
            category: 'general'
        },
        {
            label: 'Energy Capacity (kWh)',
            description: 'Battery energy capacity in kW',
            error: errors?.esEnergyCapacity,
            name: "esEnergyCapacity",
            type: "number",
            value: formData.esEnergyCapacity,
            category: 'general'
        },
        {
            label: 'Charging Efficiency',
            description: 'Percentage charging efficiency.',
            error: errors?.esChargingEff,
            name: "esChargingEff",
            type: "number",
            value: formData.esChargingEff,
            category: 'general'
        },
        {
            label: 'Discharging Efficiency',
            description: 'Percentage discharging efficiency.',
            error: errors?.esDischargingEff,
            name: "esDischargingEff",
            type: "number",
            value: formData.esDischargingEff,
            category: 'general'
        },
        {
            label: 'Charging Rate',
            description: `Charging rate. 1 means battery will fully
                charge in 1 hour if it was fully discharged.`,
            error: errors?.esChargingRate,
            name: "esChargingRate",
            type: "number",
            value: formData.esChargingRate,
            category: 'general'
        },
        {
            label: 'Discharging Rate',
            description: `Discharging rate. 1 means battery will fully 
                discharge in 1 hour if it was fully charged.`,
            error: errors?.esDischargingRate,
            name: "esDischargingRate",
            type: "number",
            value: formData.esDischargingRate,
            category: 'general'
        },
        {
            label: 'Initial Battery SOC',
            description: `Inital state of charge (SOC) for battery.
                0 means fully discharged 1 means fully charged`,
            error: errors?.esInitialSOC,
            name: "esInitialSOC",
            type: "number",
            value: formData.esInitialSOC,
            category: 'general'
        },
        {
            label: 'Power threshold for charging (% of peak power)',
            description: `When load drops below this power 
                battery starts to charge until fully charged.`,
            error: errors?.chargingPowerThreshold,
            name: "chargingPowerThreshold",
            type: "number",
            value: formData.chargingPowerThreshold,
            category: 'peak_shaving'
        },
        {
            label: 'Power threshold for discharging (% of peak power)',
            description: `When load increases below this power 
                battery starts to charge until fully discharged.`,
            error: errors?.dischargingPowerThreshold,
            name: "dischargingPowerThreshold",
            type: "number",
            value: formData.dischargingPowerThreshold,
            category: 'peak_shaving'
        },
    ]


    useDebouncedSearch(
        allTSdata,
        formData.priceProfile,
        'price',
        setSearchProfiles
    )

    return (
        <React.Fragment>
            {!closeDesView && descriptionComp}
            <div className="bg-gray-300 w-full my-10 pb-5">
                <div className="bg-blue-500 h-8 flex items-center justify-between px-2">
                    <div className="flex">
                        <img src="./images/ev_icon.svg" width="25" />
                        <p className="text-white pl-2"> {formData.name} </p>
                        <p className="w-6 h-6 bg-blue-800 text-white flex items-center 
                                justify-center pb-1 ml-5 rounded-full 
                                hover:bg-blue-600 hover:cursor-pointer"
                            onClick={() => handleEnergyStorageDelete(formData.id)}
                        > x </p>
                    </div>
                    <div
                        className="hover:cursor-pointer"
                        onClick={() => setCollapsed(value => !value)}
                    >
                        {collpased ? <img src="./images/collapse.svg" /> :
                            <img src="./images/uncollapse.svg" />}
                    </div>
                </div>

                {
                    !collpased && <React.Fragment>

                        <div className="mx-10 my-3">
                            <div className="grid grid-cols-2 md:grid-cols-3 
                                gap-y-2 mt-3 gap-x-5">

                                <FormGroupsView
                                    formFields={formFields.filter((item) =>
                                        item.category === 'general')}
                                    handleChange={handleChange}
                                />

                            </div>

                            {/* TODO: Techincal Debt to figure out better way of bundling
                            strategy and it's description section. */}
                            <div className='flex items-center gap-x-3'>
                                <div>
                                    <div className="flex items-center mt-5">
                                        <p className="pr-2"> Charging/Discharging Strategy </p>
                                        <select className="rounded-md h-8 w-32 px-2"
                                            name="esStrategy" value={formData.esStrategy}
                                            onChange={handleChange}>
                                            <option value="time">Time Based</option>
                                            {/* <option value="price">Price Based</option> */}
                                            <option value="self_consumption">Self consumption</option>
                                            <option value="peak_shaving">Peak shaving</option>
                                        </select>
                                    </div>
                                    <p className='text-sm text-gray-500 pb-2'>
                                        Pick a strategy to be used for charging and discharging a battery. </p>
                                </div>

                                <HiOutlineInformationCircle size={20}
                                    className='text-gray-500 hover:text-blue-500 hover:cursor-pointer'
                                    onClick={() => {
                                        setCloseDesView(false)
                                        setDescriptionComp(
                                            <ESStrategyDescView setCloseView={setCloseDesView} />
                                        )
                                    }}
                                />
                            </div>

                            {
                                formData.esStrategy === 'time' && <TimeFormGroupsView
                                    handleChange={handleChange}
                                    formData={formData}
                                />
                            }

                            {
                                formData.esStrategy === 'price' && <PriceGroupsView
                                    handleChange={handleChange}
                                    formData={formData}
                                    errros={errors}
                                    isClicked={isClicked}
                                    setIsClicked={setIsClicked}
                                    searchProfiles={searchProfiles}
                                    selectedPriceProfile={selectedPriceProfile}
                                    setSearchProfiles={setSearchProfiles}
                                    setSelectedPriceProfile={setSelectedPriceProfile}
                                    priceProfileExist={priceProfileExist}
                                />
                            }

                            {
                                formData.esStrategy === 'peak_shaving' && <div
                                    className="grid gap-x-5 grid-cols-2 
                                    md:grid-cols-3 gap-y-2 mt-3">
                                    <FormGroupsView
                                        formFields={formFields.filter((item) =>
                                            item.category === 'peak_shaving')}
                                        handleChange={handleChange}
                                    />
                                </div>
                            }
                        </div>


                    </React.Fragment>
                }

            </div>
        </React.Fragment>
    )
}