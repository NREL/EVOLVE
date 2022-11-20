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
        //     .test(
        //     {
        //         message: "Irradiance profile is not selected",
        //         test: function(this:any) {
        //             if (formData.technologies.includes('solar')){
        //                 return selectedIrrProfile.name ? true : false
        //             }
        //             return true
        //         }
        //     }
        // ),
    })

    const esValidationSchema  = Yup.object({
        esPowerCapacity: Yup.number().positive(),
        esEnergyCapacity: Yup.number().positive(),
        priceProfile: Yup.string()
        //     .test(    
        //     {   
        //         message: "Price profile is not selected",   
        //         test: function(this:any) {  
        //             if (this.parent.technologies.includes('energy_storage') && 
        //             this.parent.esStrategy === 'price'
        //             ){  
        //                 return selectedPriceProfile.name ? true : false
        //             }
        //             return true
        //         }
        //     }
        // ),
    })

    const basicValidationSchema:any = Yup.object({
        scenarioName: Yup.string().required().max(20),
        loadProfile: Yup.string().required(),
        //     .test(
        //     {
        //         message: "Load profile is not selected",
        //         test: function(this:any) {
        //             return selectedProfile.name ? true : false
        //         }
        //     }
        // ),
        startDate: Yup.date().min(dateRange.min).max(dateRange.max),
        endDate: Yup.date().min(Yup.ref('startDate')?Yup.ref('startDate'):dateRange.min).max(dateRange.max),
        resolution: Yup.number().positive().integer()
        //     .test({
        //     message: "Resolution should be factor of all data resolution.",
        //     test: function(this:any, val:any) {
        //         return (
        //             selectedProfile.name ? selectedProfile.resolution_min % val === 0: true &&
        //             selectedIrrProfile.name ? selectedIrrProfile.resolution_min % val === 0: true &&
        //             selectedPriceProfile.name ? selectedPriceProfile.resolution_min % val === 0: true
        //         )
        //     }
        // }),
    })

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