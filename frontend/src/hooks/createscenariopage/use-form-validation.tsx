import * as Yup from 'yup';

const useFormValidation = (
    formData:any, 
    selectedIrrProfile:any
) => {

    const solarValidationSchema:any = Yup.object({
        solarCapacity: Yup.number().positive(),
        panelAzimuth: Yup.number().min(0).max(360),
        panelTilt: Yup.number().min(-90).max(90),
        dcacRatio: Yup.number().min(0).max(2),
        irradianceData: Yup.string().test(
            {
                message: "Irradiance profile is not selected",
                test: function(this:any) {
                    if (formData.technologies.includes('solar')){
                        return selectedIrrProfile.name ? true : false
                    }
                    return true
                }
            }
        ),
    })

    return [solarValidationSchema];
}

export {useFormValidation};