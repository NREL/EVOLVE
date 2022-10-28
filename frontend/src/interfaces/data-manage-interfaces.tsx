
interface TimeSeriesDataInfoModel {
    id: number;
    name: string;
    description: string;
    created_at: string;
    start_date: string;
    end_date: string;
    resolution_min: number;
    category: string | null;
};

interface TimeSeriesDataCommentModel {
    id: number;
    data_id: number;
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




