import { useState, useEffect } from 'react';
import { newEVDataInterface } from '../../interfaces/create-scenario-interfaces';
import { v4 as uuidv4 } from 'uuid';

const UseEVForm = (
    initialState: newEVDataInterface[] | null
) => {

    const newEVData = {
        evType: "vehicle",
        evCategoryName: "Car",
        numberOfEV: 500,
        acceptedkW: "6,60",
        acceptedkWh: "8,60",
        mileage: "60,330",
        weekdayMiles: "30,60",
        weekendMiles: "50,100",
        homeCharger: 1.2,
        avergeMileage: 15,
        weekdayTravelHours: "9,17",
        weekendTravelHours: "12,19",
        intialSocs: "80,100",
        stationCategoryName: "Level 2 Chargers",
        numberOfStations: 5,
        numberOfSlots: "5,10",
        maxSlotkW: 9.6
    }

    const [counter, setCounter] = useState(2)

    const [evFormDataArray, setEVFormDataArray] = useState<newEVDataInterface[]>([{
        ...newEVData, id: uuidv4(), name: 'EV 1'
    }])

    const [evErrorsArray, setEVErrorsArray] = useState<Record<string, any>[]>([{}])

    const handleAddEV = () => {
        setCounter(val => val + 1)
        setEVFormDataArray((arr: any[]) => [...arr, {
            ...newEVData, id: uuidv4(), name: `EV ${counter}`
        }])
        setEVErrorsArray((arr: any[]) => [...arr, {}])
    }

    const handleEVDelete = (id: string) => {
        const itemIndex = evFormDataArray.findIndex(arr => arr.id === id)
        setEVFormDataArray(arr => arr.filter((x, index) => index !== itemIndex))
        setEVErrorsArray(arr => arr.filter((x, index) => index !== itemIndex))
        console.log(itemIndex)
    }

    useEffect(() => {
        if (initialState) {
            setEVFormDataArray(initialState)
            setEVErrorsArray(Array(initialState.length).fill({}))
        }
    }, [initialState])

    return [evFormDataArray, setEVFormDataArray,
        evErrorsArray, setEVErrorsArray, handleAddEV,
        handleEVDelete] as const;
}

export { UseEVForm };