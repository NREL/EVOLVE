interface ReportDataInterface {
    id: number;
    created_at: string;
    name: string;
    description: string;
    status: string;
}

interface BaseLoadTSDataInterface {
   timestamp: string[];
   kW: number[];
}

export {
    ReportDataInterface,
    BaseLoadTSDataInterface
}