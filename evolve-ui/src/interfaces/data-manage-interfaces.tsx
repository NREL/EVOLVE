
interface TimeSeriesDataInfoModel {
    id: number;
    name: string;
    description: string;
    created_at: string;
    start_date: string;
    end_date: string;
    resolution_min: number;
    category: string | null;
    owner: string;
    shared_users: {
       username: string;
       shared_date: string; 
    }[]
};

interface TimeSeriesDataCommentModel {
    id: number;
    timeseriesdata_id: number;
    comment: string;
    edited: boolean;
    username: string;
    created_at: string;
    updated_at: string;
};

enum DateSortString {
    descending = 'descending',
    ascending = 'ascending'
};

enum TimeSeriesDataCategory {
    kW = 'kW',
    irradiance = 'irradiance'
};

export {
    TimeSeriesDataInfoModel,
    TimeSeriesDataCommentModel,
    DateSortString,
    TimeSeriesDataCategory
};




