import React from 'react';
import Plot from 'react-plotly.js';

interface TimeseriesPowerViewProps {
    tsPower: any;
    title: string;
}

export const TimeseriesPowerView: React.FC<TimeseriesPowerViewProps> = ({
    tsPower, title
}) => {

    const names = tsPower?.timestamp.length ?
        Object.keys(tsPower).filter((d) => d != 'timestamp') : []

    const timeSeriesData = names.map((item) => {
        return {
            x: tsPower.timestamp, y: tsPower[item],
            type: 'scatter', mode: 'lines',
            name: item
        }
    })

    return (
        <div>
            {

                timeSeriesData && <Plot
                    data={timeSeriesData}
                    className="w-full h-[350px]"
                    layout={{
                        margin: { b: 50, l: 60, r: 60, t: 50 },
                        title: title,
                        yaxis: { title: title },
                        legend: { "orientation": "h",x:0, y:-0.2 }
                    }}
                />
            }
            {

                !timeSeriesData && <div className="w-full h-[350px]
                                        bg-gray-200 animate-pulse flex justify-center items-center">
                    <div className="w-10 h-20 bg-gray-300 mr-3"></div>
                    <div className="w-10 h-40 bg-gray-300 mr-3"></div>
                    <div className="w-10 h-10 bg-gray-300"></div>
                </div>
            }
        </div>
    );
}