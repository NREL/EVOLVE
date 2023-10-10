import React, { useState } from 'react';
import { TextField } from '../../components/text-field';
import { FormGroupsView } from './utils';

export function EVSettingsView(props: any) {
    const { formData, handleChange, errors, handleEVDelete } = props;
    const [collpased, setCollapsed] = useState(false);

    const formFields = [
        {
            label: 'EV Catgeory Name',
            description: `Specify category name for this group of vehicles. e.g Cars`,
            error: errors?.evCategoryName,
            name: "evCategoryName",
            type: "text",
            value: formData.evCategoryName,
            evtype: "vehicle"
        },
        {
            label: 'Number of vehicles',
            description: `Estimated number
            of electric vehicles.`,
            error: errors?.numberOfEV,
            name: "numberOfEV",
            type: "number",
            value: formData.numberOfEV,
            evtype: "vehicle"
        },
        {
            label: 'Accepted kW Range',
            description: `Exact accepted kw for each vehicle will be randomly sampled
            to fall within the range you specified. e.g. 6,9`,
            error: errors?.acceptedkW,
            name: "acceptedkW",
            type: "text",
            value: formData.acceptedkW,
            evtype: "vehicle"
        },
        {
            label: 'Accepted kWh Range',
            description: `Exact energy capacity (kwh) for each vehicle will be randomly sampled
            to fall within the range you specified. e.g. 30, 60`,
            error: errors?.acceptedkWh,
            name: "acceptedkWh",
            type: "text",
            value: formData.acceptedkWh,
            evtype: "vehicle"
        },
        {
            label: 'Mileage Range',
            description: `Exact mileage (how many miles can be 
                driven with fully charged battery) for each vehicle will be randomly sampled
                to fall within the range you specified. e.g. 60, 250`,
            error: errors?.mileage,
            name: "mileage",
            type: "text",
            value: formData.mileage,
            evtype: "vehicle"
        },
        {
            label: 'Weekday Tarvel Miles Range',
            description: `Miles travelled during weekday. Specific miles for each vehicle is 
                determined using random sampling. `,
            error: errors?.weekdayMiles,
            name: "weekdayMiles",
            type: "text",
            value: formData.weekdayMiles,
            evtype: "vehicle"
        },
        {
            label: 'Weekend Tarvel Miles Range',
            description: `Miles travelled during weekend. Specific miles for each vehicle is 
                determined using random sampling. `,
            error: errors?.weekendMiles,
            name: "weekendMiles",
            type: "text",
            value: formData.weekendMiles,
            evtype: "vehicle"
        },
        {
            label: 'Home Charger (kW)',
            description: `Maximum home charger capacity.`,
            error: errors?.homeCharger,
            name: "homecharger",
            type: "number",
            value: formData.homeCharger,
            evtype: "vehicle"
        },
        {
            label: 'Average Mile Per Hour',
            description: `Average mile travelled per hour`,
            error: errors?.avergeMileage,
            name: "avergeMileage",
            type: "number",
            value: formData.avergeMileage,
            evtype: "vehicle"
        },
        {
            label: 'Weekday Travel Hours',
            description: `Travel hours for weekday. Please use numbers between 0 and 23. e.g. 9, 17`,
            error: errors?.weekdayTravelHours,
            name: "weekdayTravelHours",
            type: "text",
            value: formData.weekdayTravelHours,
            evtype: "vehicle"
        },
        {
            label: 'Weekend Travel Hours',
            description: `Travel hours for weekend. Please use numbers 
            between 0 and 23. e.g. 12, 18`,
            error: errors?.weekendTravelHours,
            name: "weekendTravelHours",
            type: "text",
            value: formData.weekendTravelHours,
            evtype: "vehicle"
        },
        {
            label: 'Initial SOCs Range',
            description: `Range of initial state of charges (SOCs)`,
            error: errors?.intialSocs,
            name: "intialSocs",
            type: "text",
            value: formData.intialSocs,
            evtype: "vehicle"
        },
        {
            label: 'Initial SOCs Range',
            description: `Range of initial state of charges (SOCs)`,
            error: errors?.intialSocs,
            name: "intialSocs",
            type: "text",
            value: formData.intialSocs,
            evtype: "vehicle"
        },
        {
            label: 'Station Catgeory Name',
            description: `Specify category name for this group of stations. e.g Level 2 Chargers`,
            error: errors?.stationCategoryName,
            name: "stationCategoryName",
            type: "text",
            value: formData.stationCategoryName,
            evtype: "charging_station"
        },
        {
            label: 'Number of Stations',
            description: `Specify number of stations of this type.`,
            error: errors?.numberOfStations,
            name: "numberOfStations",
            type: "number",
            value: formData.numberOfStations,
            evtype: "charging_station"
        },
        {
            label: 'Number of Slots Range',
            description: `Range of number of slots. e.g. 3, 6 per station.`,
            error: errors?.numberOfSlots,
            name: "numberOfSlots",
            type: "text",
            value: formData.numberOfSlots,
            evtype: "charging_station"
        },
        {
            label: 'Maximum Charger kW Per Slot',
            description: `Maximum accepted kW for station.`,
            error: errors?.maxSlotkW,
            name: "maxSlotkW",
            type: "number",
            value: formData.maxSlotkW,
            evtype: "charging_station"
        }
    ]

    return (
        <React.Fragment>
            <div className="bg-gray-300 w-full my-10 pb-5">
                <div className="bg-blue-500 h-8 flex items-center justify-between px-2">
                    <div className="flex">
                        <img src="./images/ev_icon.svg" width="25" />
                        <p className="text-white pl-2"> {formData.name} </p>
                        <p className="w-6 h-6 bg-blue-800 text-white flex items-center 
                                justify-center pb-1 ml-5 rounded-full hover:bg-blue-600 hover:cursor-pointer"
                            onClick={() => handleEVDelete(formData.id)}
                        > x </p>
                    </div>
                    <div
                        className="hover:cursor-pointer"
                        onClick={() => setCollapsed(value => !value)}
                    >
                        {collpased ? <img src="./images/collapse.svg" /> : <img src="./images/uncollapse.svg" />}
                    </div>
                </div>

                <div className='px-10'>
                    <div className="flex items-center mt-5 ">
                        <p className="pr-2"> Select Vehicle or Charging Station </p>
                        <select className="rounded-md h-8 w-32 px-2"
                            name="evType" value={formData.evType}
                            onChange={handleChange}>
                            <option value="vehicle">Vehicle</option>
                            <option value="charging_station">Charging Station</option>
                        </select>
                    </div>
                    <p className='text-sm text-gray-500 pb-2'>
                        Pick whether you want to model electric vehicle or
                        charging stattions.  </p>
                </div>

                {
                    !collpased && <React.Fragment>
                        <div className="grid grid-cols-2 md:grid-cols-3 mx-10 my-3 gap-y-2 gap-x-5">

                            <FormGroupsView
                                formFields={formFields.filter((item: any) => item.evtype == formData.evType)}
                                handleChange={handleChange}
                            />

                        </div>
                    </React.Fragment>
                }


            </div>
        </React.Fragment>
    )
}