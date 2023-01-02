import { useEffect, useState } from 'react';
import { newBasicDataInterface } from '../../interfaces/create-scenario-interfaces';
import { TimeSeriesDataInfoModel } from '../../interfaces/data-manage-interfaces';

const UseBasicForm = (
    initialState: newBasicDataInterface | null,
    initialSelectedProfile: TimeSeriesDataInfoModel | null
) => {
    // console.log('initial profile', initialSelectedProfile)
    const newBasicData = {
        scenarioName: '',
        technologies: [],
        loadProfile: '',
        startDate: null,
        endDate: null,
        resolution: 1,
        dataFillingStrategy: 'interpolation',
    }

    const [formData, setFormData] = useState<newBasicDataInterface>(
        initialState ? initialState : newBasicData)

    const [errors, setErrors] = useState<Record<string, string>>({})

    const [selectedProfile, setSelectedProfile] = useState<TimeSeriesDataInfoModel | null>(null)

    const [fillData, setFillData] = useState(false)

    const [dateRange, setDateRange] = useState({
        min: "1990-01-01",
        max: "2050-01-01"
    })

    useEffect(() => {
        initialSelectedProfile && setSelectedProfile(initialSelectedProfile)
    }, [initialSelectedProfile])

    return [formData, setFormData, errors, setErrors,
        selectedProfile, setSelectedProfile, fillData,
        setFillData, dateRange, setDateRange] as const;
}

export { UseBasicForm };