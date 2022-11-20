import { useState } from 'react';
import {newBasicDataInterface} from '../../interfaces/create-scenario-interfaces';

const UseBasicForm = () => {

    const newBasicData = {
        scenarioName: '',
        technologies: [],
        loadProfile: '',
        startDate: null,
        endDate: null,
        resolution: 1,
        dataFillingStrategy: 'interpolation',
    }

    const [formData, setFormData] = useState<newBasicDataInterface>(newBasicData)
    const [errors, setErrors] = useState<Record<string, string>>({})

    const [selectedProfile, setSelectedProfile] = useState<Record<string, any>>({})
    const [fillData, setFillData] = useState(false)

    const [dateRange, setDateRange] = useState({
        min: "1990-01-01",
        max: "2050-01-01"
    })

    return [formData, setFormData, errors, setErrors,
        selectedProfile, setSelectedProfile, fillData, 
        setFillData, dateRange, setDateRange] as const;
}

export {UseBasicForm};