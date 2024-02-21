import { TimeSeriesDataInfoModel } from "./data-manage-interfaces"

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
    evType: string
    evCategoryName: string
    name: string
    numberOfEV: number
    acceptedkW: string
    acceptedkWh: string
    mileage: string
    weekdayMiles: string
    weekendMiles: string
    homeCharger: number
    avergeMileage: number
    weekdayTravelHours: string
    weekendTravelHours: string
    intialSocs: string
    stationCategoryName: string
    numberOfStations: number
    numberOfSlots: string
    maxSlotkW: number
}

interface newBasicDataInterface {
    scenarioName: string
    technologies: string[]
    loadProfile: string
    startDate: Date | null
    endDate: Date | null
    resolution: number
    dataFillingStrategy: string
    scenarioDescription: string
}

interface scenarioJSONInterface {
    basic: {
        scenarioName: string;
        technologies: string[];
        loadProfile: number;
        startDate: string;
        endDate: string;
        resolution: number;
        dataFillingStrategy: string;
    };
    solar?: newSolarDataInterface[];
    ev?: newEVDataInterface[];
    energy_storage?: newESDataInterface[];
}

interface profileInterface {
    name: string;
    data: TimeSeriesDataInfoModel | null;
}

export {
    newSolarDataInterface,
    newESDataInterface,
    newEVDataInterface,
    newBasicDataInterface,
    scenarioJSONInterface,
    profileInterface
}