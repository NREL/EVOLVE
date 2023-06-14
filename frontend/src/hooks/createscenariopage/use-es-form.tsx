import { v4 as uuidv4 } from 'uuid';
import { useState, useEffect } from 'react';
import { newESDataInterface } from '../../interfaces/create-scenario-interfaces';
import { profileInterface } from '../../interfaces/create-scenario-interfaces';

const UseESForm = (
    initialState: newESDataInterface[] | null,
    initialPriceProfiles: profileInterface[] | null
) => {

    const newESData = {
        esPowerCapacity: 10,
        esEnergyCapacity: 10,
        esStrategy: 'time',
        chargingHours: [],
        disChargingHours: [],
        chargingPrice: 0,
        disChargingPrice: 0,
        priceProfile: '',
        chargingPowerThreshold: 70,
        dischargingPowerThreshold: 80,
        esChargingEff: 0.95,
        esDischargingEff: 0.95,
        esChargingRate: 0.5,
        esDischargingRate: 0.5,
        esInitialSOC: 0.5
    }

    const [counter, setCounter] = useState(2)

    const [esFormDataArray, setESFormDataArray] = useState<newESDataInterface[]>([{
        ...newESData, id: uuidv4(), name: 'Energy Storage 1'
    }])

    const [esErrorsArray, setESErrorsArray] = useState<Record<string, any>[]>([{}])
    const [selectedPriceProfile, setSelectedPriceProfile] = useState<Record<string, any>[]>([
        {
            name: 'Energy Storage 1',
            data: {}
        }
    ])

    const handleAddEnergyStorage = () => {
        setCounter(val => val + 1)
        setESFormDataArray((arr: any[]) => [...arr, {
            ...newESData, id: uuidv4(), name: `Energy Storage ${counter}`
        }])
        setESErrorsArray((arr: any[]) => [...arr, {}])
    }

    const handleEnergyStorageDelete = (id: string) => {
        const itemIndex = esFormDataArray.findIndex(arr => arr.id === id)
        setESFormDataArray(arr => arr.filter((x, index) => index !== itemIndex))
        setESErrorsArray(arr => arr.filter((x, index) => index !== itemIndex))
        console.log(itemIndex)
    }

    useEffect(() => {
        initialState && setESFormDataArray(initialState)
    }, [initialState])

    useEffect(() => {
        initialPriceProfiles && setSelectedPriceProfile(initialPriceProfiles)
    }, [initialPriceProfiles])

    return [esFormDataArray, setESFormDataArray,
        esErrorsArray, setESErrorsArray, handleAddEnergyStorage,
        handleEnergyStorageDelete, selectedPriceProfile, setSelectedPriceProfile] as const;

}

export { UseESForm };