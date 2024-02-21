import React, { useEffect, useState } from 'react';

const UseSelectedProfile = (
    resolution: number,
    selectedProfile: any,
    selectedIrrProfile: any,
    selectedPriceProfile: any,
    setDateRange: any,
    setFillData: any
) => {
    // Use effect to update data resolution
    useEffect(() => {

        const maxDataResolution = Math.max(...[
            selectedProfile ? selectedProfile.resolution_min : 0,
            ...selectedIrrProfile.map((d: Record<string, any>) => d.data && d.data.resolution_min ? d.data.resolution_min : 0),
            ...selectedPriceProfile.map((d: Record<string, any>) => d.data && d.data.resolution_min ? d.data.resolution_min : 0)
        ])

        if (maxDataResolution !== 0 && resolution < maxDataResolution) {
            setFillData(true)
        } else {
            setFillData(false)
        }

    }, [
        resolution,
        selectedProfile,
        selectedIrrProfile,
        selectedPriceProfile
    ])

    // Use effect to update date range

    useEffect(() => {
        if (selectedProfile || selectedIrrProfile || selectedPriceProfile) {

            setDateRange({
                min: new Date(Math.max(...[
                    new Date(selectedProfile ?
                        selectedProfile.start_date : '1990-01-01').getTime(),
                    ...selectedIrrProfile.map((d: Record<string, any>) => new Date(d.data && d.data.start_date ? d.data.start_date : "1990-01-01").getTime()),
                    ...selectedPriceProfile.map((d: Record<string, any>) => new Date(d.data && d.data.start_date ? d.data.start_date : "1990-01-01").getTime())
                ])).toISOString().split('T')[0],
                max: new Date(Math.min(...[
                    new Date(selectedProfile ?
                        selectedProfile.end_date : "2050-01-01").getTime(),
                    ...selectedIrrProfile.map((d: Record<string, any>) => new Date(d.data && d.data.end_date ? d.data.end_date : "2050-01-01").getTime()),
                    ...selectedPriceProfile.map((d: Record<string, any>) => new Date(d.data && d.data.end_date ? d.data.end_date : "2050-01-01").getTime())
                ])).toISOString().split('T')[0]
            })
        } else {
            setDateRange({
                min: "1990-01-01",
                max: "2050-01-01"
            })
        }

    }, [selectedProfile, selectedIrrProfile, selectedPriceProfile])

}

export { UseSelectedProfile };