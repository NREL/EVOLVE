import React from 'react';
import Plot from 'react-plotly.js';
import { SortObject } from './helper';

interface EnergyMetricsViewProps {
    metric: any;
    title: string;
}

export const EnergyMetricsView: React.FC<EnergyMetricsViewProps> = ({
    metric, title
}) => {

    const metric_ = SortObject(metric);
    const metricData = metric_ ? Object.keys(metric_).filter(
        (item:string)=> !['category', 'timestamp'].includes(item)).map((item:string)=> {
            return {
                x: metric_ && metric_?.timestamp ? metric_.timestamp : metric_.category,
                y: metric_[item].map((val:number)=> Math.abs(val) ),
                type: 'bar',
                name: item
            }
        }): [];

    return (
        <div className='w-100'>
            {

                metricData.length >0  && <Plot
                    data={metricData}
                    layout={{
                        barmode: 'group',
                        margin: {b:50, l:60, r:20, t:50},
                        title: "Timeseries Aggregated Energy",
                        yaxis: {title: title},
                        legend: {"orientation": "h", x: 1, y:-0.2}
                    }}
                className="w-full h-[350px] mb-5"
                />
            }
            {

                !metricData && <div className="w-full h-[350px]
                                        bg-gray-200 animate-pulse flex justify-center items-center">
                    <div className="w-10 h-20 bg-gray-300 mr-3"></div>
                    <div className="w-10 h-40 bg-gray-300 mr-3"></div>
                    <div className="w-10 h-10 bg-gray-300"></div>
                </div>
            }
        </div>
    );
}