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
    esPowerCapacity: number
    esEnergyCapacity: number
    esStrategy: string
    chargingHours: number[]
    disChargingHours: number[]
    chargingPrice: number
    disChargingPrice: number
    priceProfile: string
    chargingPowerThreshold: number
    dischargingPowerThreshold: number
}

interface newEVDataInterface {
    id: string
    name: string 
    numberOfEV: number
    pctResEV: number
}

interface newBasicDataInterface {
    scenarioName: string
    technologies: string[]
    loadProfile: string
    startDate: Date | null
    endDate: Date | null
    resolution: number
    dataFillingStrategy: string
}

export {
    newSolarDataInterface,
    newESDataInterface,
    newEVDataInterface,
    newBasicDataInterface
}