import { useState } from 'react';
import {newSolarDataInterface} from '../../interfaces/create-scenario-interfaces';
import { v4 as uuidv4 } from 'uuid';

const UseSolarForm = () => {

    const newSolarData = {
        solarCapacity: 10,
        irradianceData: "",
        panelAzimuth: 0,
        panelTilt: 0,
        solarInstallationStrategy: 'fixed',
        dcacRatio: 1,
    }

    const [counter, setCounter] = useState(2)
    

    const [solarFormDataArray, setSolarFormDataArray] = useState<newSolarDataInterface[]>([
        {...newSolarData, id: uuidv4(), name: 'Solar 1'}
    ])
    const [solarErrorsArray, setSolarErrorsArray] = useState<Record<string, any>[]>([{}])
    const [selectedIrrProfile, setSelectedIrrProfile] = useState<Record<string, any>[]>([{
        name: 'Solar 1',
        data: {}
    }])

    const handleAddSolar = () => {
        setCounter(val=> val+1)
        setSolarFormDataArray( (arr:any[]) => [...arr, {
            ...newSolarData, id: uuidv4(), name:`Solar ${counter}`
        }])
        setSolarErrorsArray((arr:any[]) => [...arr, {}])
        setSelectedIrrProfile( (arr:any[]) => [
            ...arr, {
                name: `Solar ${counter}`,
                data: {}
            }
        ])
    }

    const handleSolarDelete = (id:string) => {
        const itemIndex = solarFormDataArray.findIndex(arr=> arr.id === id)
        setSolarFormDataArray(arr=> arr.filter((x, index)=> index !== itemIndex ))
        setSolarErrorsArray(arr=> arr.filter((x, index)=> index !== itemIndex ))
        setSelectedIrrProfile((arr:any[])=> arr.filter((x, index)=> index !== itemIndex))
    }

    return [solarFormDataArray, setSolarFormDataArray,
        solarErrorsArray, setSolarErrorsArray, handleAddSolar, 
        handleSolarDelete, selectedIrrProfile, setSelectedIrrProfile] as const;
}

export {UseSolarForm};