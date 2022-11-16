interface newSolarDataInterface {
    id: string
    name: string
    solarCapacity: number
    irradianceData: string
    panelAzimuth: number
    panelTilt: number
    solarInstallationStrategy: string
    dcacRatio: number
}

interface newESDataInterface {
    id: string
    name: string
    isESOptimal: boolean
    esPowerCapacity: number
    esEnergyCapacity: number
    esStrategy: string
    chargingHours: number[]
    disChargingHours: number[]
    chargingPrice: number
    disChargingPrice: number
    priceProfile: string
    esChargingThreshold: number
    esDischargingThreshold: number
    chargingPowerThreshold: number
    dischargingPowerThreshold: number
}

export {
    newSolarDataInterface,
    newESDataInterface
}