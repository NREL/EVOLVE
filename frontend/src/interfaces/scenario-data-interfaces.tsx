interface ScenarioDataInterface {
    id: number
    created_at: string
    name: string
    description: string
    solar: boolean
    ev: boolean
    storage: boolean
    filename: string
}

export {
    ScenarioDataInterface
}