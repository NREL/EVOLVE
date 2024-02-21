import * as Yup from 'yup';



const useFormValidation = (
    dateRange: any
) => {

    const solarValidationSchema: any = Yup.object({
        solarCapacity: Yup.number().positive(),
        panelAzimuth: Yup.number().min(0).max(360),
        panelTilt: Yup.number().min(-90).max(90),
        dcacRatio: Yup.number().min(0).max(2),
        longitude: Yup.number().min(-180).max(180),
        latitude: Yup.number().min(-90).max(90),
        irradianceData: Yup.string()
    })

    const esValidationSchema = Yup.object({
        esPowerCapacity: Yup.number().positive(),
        esEnergyCapacity: Yup.number().positive(),
        esChargingEff: Yup.number().positive().min(0.5).max(1.0),
        esDischargingEff: Yup.number().positive().min(0.5).max(1.0),
        esChargingRate: Yup.number().positive().min(0.05).max(50.0),
        esDischargingRate: Yup.number().positive().min(0.05).max(50.0),
        esInitialSOC: Yup.number().positive().min(0).max(1.0),
        priceProfile: Yup.string()
    })

    const basicValidationSchema: any = Yup.object({
        scenarioName: Yup.string().required().max(255),
        loadProfile: Yup.string().required(),
        startDate: Yup.date().min(dateRange.min).max(dateRange.max),
        endDate: Yup.date().min(Yup.ref('startDate') ? Yup.ref('startDate') : dateRange.min).max(dateRange.max),
        resolution: Yup.number().positive().integer()
    })

    const evValidationSchema: any = Yup.object({
        numberOfEV: Yup.number().positive(),
        maxSlotkW: Yup.number().min(1).max(300),
        homeCharger: Yup.number().min(1).max(20),
        acceptedkW: Yup.string().trim(),
        acceptedkWh: Yup.string().trim(),
        mileage: Yup.string().trim(),
        weekdayMiles: Yup.string().trim(),
        weekendMiles: Yup.string().trim(),
        weekdayTravelHours: Yup.string().trim(),
        weekendTravelHours: Yup.string().trim(),
        intialSocs: Yup.string().trim(),
        numberOfSlots: Yup.string().trim()
    })

    return [solarValidationSchema,
        esValidationSchema,
        basicValidationSchema,
        evValidationSchema
    ];

}

export { useFormValidation };