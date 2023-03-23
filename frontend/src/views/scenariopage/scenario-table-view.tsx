import React, { useEffect } from 'react';
import {
    scenarioJSONInterface, newESDataInterface, newEVDataInterface, newSolarDataInterface
} from '../../interfaces/create-scenario-interfaces';


interface ScenarioTableViewProps {
    scenJSON: scenarioJSONInterface;
    setIsViewClicked: React.Dispatch<React.SetStateAction<boolean>>;
}

export const ScenarioTableView: React.FC<ScenarioTableViewProps> = ({
    scenJSON, setIsViewClicked
}) => {

    return (
        <div className="w-full py-10 px-20">
            <div className="bg-gray-100 p-10 shadow-md h-[100vh-10rm overflow-y-scroll relative">
                <div className="absolute right-3 top-2 bg-gray-300 rounded-full 
                    w-8 h-8 flex justify-center items-center hover:cursor-pointer hover:bg-gray-400"
                    onClick={() => setIsViewClicked(false)}> X </div>
                {
                    scenJSON.basic && <h1 className="text-indigo-500 font-bold border-b border-indigo-500 mb-5">
                        {scenJSON.basic.scenarioName}</h1>
                }
                {
                    scenJSON.basic && <div>
                        <h1 className="border-b mb-5 bg-orange-600 w-max border-slate-200 px-2 py-1 
                            rounded-md shadow-md text-white"> Load profile  </h1>
                        <table className='w-full table-auto border-collapse'>
                            <tr className="bg-gray-500 h-10">
                                <th> Load Profile </th>
                                <th> Start Date </th>
                                <th> End Date</th>
                                <th> Resolution (min.) </th>
                                <th> Data Filling Strategy </th>
                            </tr>

                            <tr className="h-10 bg-gray-300 text-center">
                                <td> {scenJSON.basic.loadProfile} </td>
                                <td> {scenJSON.basic.startDate} </td>
                                <td> {scenJSON.basic.endDate} </td>
                                <td> {scenJSON.basic.resolution} </td>
                                <td> {scenJSON.basic.dataFillingStrategy} </td>
                            </tr>
                        </table>
                    </div>
                }
                {
                    scenJSON.solar && scenJSON.solar.length > 0 && <div>
                        <h1 className="border-b my-5 bg-orange-600 w-max border-slate-200 px-2 py-1 
                            rounded-md shadow-md text-white"> Solar Units </h1>
                        <table className='w-full table-auto border-collapse'>
                            <tr className="bg-gray-500 h-10">
                                <th> Name </th>
                                <th> Capacity (kW) </th>
                                <th> Installaion type</th>
                                <th> Azimuth </th>
                                <th> Tilt </th>
                                <th> DC/AC ratio</th>
                            </tr>

                            {
                                scenJSON.solar.map(
                                    (value: newSolarDataInterface) => {
                                        return <tr className="h-10 bg-gray-300 text-center" key={value.id}>
                                            <td> {value.name} </td>
                                            <td> {value.solarCapacity} </td>
                                            <td> {value.solarInstallationStrategy} </td>
                                            <td> {value.panelAzimuth} </td>
                                            <td> {value.panelTilt} </td>
                                            <td> {value.dcacRatio} </td>
                                        </tr>
                                    }
                                )
                            }
                        </table>
                    </div>
                }
                {
                    scenJSON.ev && scenJSON.ev.length > 0 && <div>
                        <h1 className="border-b my-5 bg-orange-600 w-max border-slate-200 px-2 py-1 
                            rounded-md shadow-md text-white"> Electric Vehicle Units </h1>
                        <table className='w-full table-auto border-collapse'>
                            <tr className="bg-gray-500 h-10">
                                <th> Number of EV units </th>
                                <th> % Residential EV </th>
                            </tr>

                            {
                                scenJSON.ev.map(
                                    (value: newEVDataInterface, index: number) => {
                                        return <tr className="h-10 bg-gray-300 text-center" key={'ev_' + index}>
                                            <td> {value.numberOfEV} </td>
                                            <td> {value.pctResEV} </td>
                                        </tr>
                                    }
                                )
                            }
                        </table>
                    </div>
                }
                {
                    scenJSON.energy_storage && scenJSON.energy_storage.length > 0 && <div>
                        <h1 className="border-b my-5 bg-orange-600 w-max border-slate-200 px-2 py-1 
                            rounded-md shadow-md text-white"> Electric Storage Units </h1>

                        <p className="text-indigo-600 mb-2 border-b-2 border-indigo-500 w-max"> Electric storage with user defined
                            charging and discharging powers </p>
                        <table className='w-full table-auto border-collapse'>
                            <tr className="bg-gray-500 h-10">
                                <th> Name </th>
                                <th> Strategy </th>
                                <th> Charging Hours </th>
                                <th> Discharging hours </th>
                                <th> Maximum discharge kW </th>
                                <th> Capacity (kWh) </th>
                            </tr>

                            {
                                scenJSON.energy_storage.map(
                                    (value: newESDataInterface) => {
                                        return value.esStrategy === 'time' && <tr className="h-10 bg-gray-300 text-center" key={value.id}>
                                            <td> {value.name} </td>
                                            <td> {value.esStrategy} </td>
                                            <td> {value.chargingHours.join(', ')} </td>
                                            <td> {value.disChargingHours.join(', ')} </td>
                                            <td> {value.esPowerCapacity} </td>
                                            <td> {value.esEnergyCapacity} </td>
                                        </tr>
                                    }
                                )
                            }
                        </table>

                        <p className="text-indigo-600 my-2 border-b-2 border-indigo-500 w-max"> Electric storage with user defined power
                            thresholds for charging and discharging </p>
                        <table className='w-full table-auto border-collapse mt-3'>
                            <tr className="bg-gray-500 h-10">
                                <th> Name </th>
                                <th> Strategy </th>
                                <th> Charging Power Thresh. </th>
                                <th> Discharging Power Thresh. </th>
                                <th> Maximum discharge kW </th>
                                <th> Capacity (kWh) </th>
                            </tr>

                            {
                                scenJSON.energy_storage.map(
                                    (value: newESDataInterface) => {
                                        return value.esStrategy === 'peak_shaving' && <tr className="h-10 bg-gray-300 text-center" key={value.id}>
                                            <td> {value.name} </td>
                                            <td> {value.esStrategy} </td>
                                            <td> {value.chargingPowerThreshold} </td>
                                            <td> {value.dischargingPowerThreshold} </td>
                                            <td> {value.esPowerCapacity} </td>
                                            <td> {value.esEnergyCapacity} </td>
                                        </tr>
                                    }
                                )
                            }
                        </table>

                        <p className="text-indigo-600 my-2 border-b-2 border-indigo-500 w-max"> Electric storage with user defined price
                            thresholds for charging and discharging </p>
                        <table className='w-full table-auto border-collapse mt-3'>
                            <tr className="bg-gray-500 h-10">
                                <th> Name </th>
                                <th> Strategy </th>
                                {/* <th> Charging Price Thresh. </th>
                                <th> Discharging Price Thresh. </th> */}
                                <th> Maximum discharge kW </th>
                                <th> Capacity (kWh) </th>
                            </tr>

                            {
                                scenJSON.energy_storage.map(
                                    (value: newESDataInterface) => {
                                        return value.esStrategy === 'self_consumption' && <tr className="h-10 bg-gray-300 text-center" key={value.id}>
                                            <td> {value.name} </td>
                                            <td> {value.esStrategy} </td>
                                            {/* <td> {value.chargingPrice} </td>
                                            <td> {value.disChargingPrice} </td> */}
                                            <td> {value.esPowerCapacity} </td>
                                            <td> {value.esEnergyCapacity} </td>
                                        </tr>
                                    }
                                )
                            }
                        </table>
                    </div>
                }
                {/* {JSON.stringify(scenJSON, null, 2)} */}
            </div>
        </div>
    );
}