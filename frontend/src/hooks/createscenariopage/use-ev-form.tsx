import { useState } from 'react';
import {newEVDataInterface} from '../../interfaces/create-scenario-interfaces';
import { v4 as uuidv4 } from 'uuid';

const UseEVForm = () => {

    const newEVData = {
        numberOfEV: 1,
        pctResEV: 100
    }

    const [counter, setCounter] = useState(2)

    const [evFormDataArray, setEVFormDataArray] = useState<newEVDataInterface[]>([{
        ...newEVData, id: uuidv4(), name:'EV 1'
    }])

    const [evErrorsArray, setEVErrorsArray] = useState<Record<string, any>[]>([{}])

    const handleAddEV = () => {
        setCounter(val=> val+1)
        setEVFormDataArray( (arr:any[]) => [...arr, {
            ...newEVData, id: uuidv4(), name:`EV ${counter}`
        }])
        setEVErrorsArray((arr:any[]) => [...arr, {}])
    }

    const handleEVDelete = (id:string) => {
        const itemIndex = evFormDataArray.findIndex(arr=> arr.id === id)
        setEVFormDataArray(arr=> arr.filter((x, index)=> index !== itemIndex ))
        setEVErrorsArray(arr=> arr.filter((x, index)=> index !== itemIndex ))
        console.log(itemIndex)
    }

    return [evFormDataArray, setEVFormDataArray,
        evErrorsArray, setEVErrorsArray, handleAddEV, 
        handleEVDelete] as const;
}

export {UseEVForm};