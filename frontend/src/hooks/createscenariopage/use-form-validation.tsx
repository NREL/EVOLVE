import * as Yup from 'yup';

const useFormValidation = (
    dateRange: any
) => {

    const solarValidationSchema:any = Yup.object({
        solarCapacity: Yup.number().positive(),
        panelAzimuth: Yup.number().min(0).max(360),
        panelTilt: Yup.number().min(-90).max(90),
        dcacRatio: Yup.number().min(0).max(2),
        irradianceData: Yup.string()
    })

    const esValidationSchema  = Yup.object({
        esPowerCapacity: Yup.number().positive(),
        esEnergyCapacity: Yup.number().positive(),
        priceProfile: Yup.string()
    })

    const basicValidationSchema:any = Yup.object({
        scenarioName: Yup.string().required().max(20),
        loadProfile: Yup.string().required(),
        startDate: Yup.date().min(dateRange.min).max(dateRange.max),
        endDate: Yup.date().min(Yup.ref('startDate')?Yup.ref('startDate'):dateRange.min).max(dateRange.max),
        resolution: Yup.number().positive().integer()})

    const evValidationSchema:any = Yup.object({
        numberOfEV: Yup.number().positive(),
        pctResEV: Yup.number().min(0).max(100)
    })

    return [solarValidationSchema, 
        esValidationSchema,
        basicValidationSchema,
        evValidationSchema
    ];

}

export {useFormValidation};