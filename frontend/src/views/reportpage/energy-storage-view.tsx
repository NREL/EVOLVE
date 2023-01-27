import React from 'react';
import Plot from 'react-plotly.js';

interface ESViewProps {
        batteryPower: any
}

export const ESView: React.FC<ESViewProps> = ({
    batteryPower
}) => {

        const storage_names = batteryPower?.timestamp.length? 
            Object.keys(batteryPower).filter((d)=> d!='timestamp'): []
        const ESTimeSeriesData =  storage_names.map((item) => {
                return { x: batteryPower.timestamp, y: batteryPower[item],
                        type: 'scatter', mode: 'lines',
                        name: item}
            })
       

        return (
                <div>
                        {

                                <Plot
                                        data={ESTimeSeriesData}
                                        className="w-[calc(100vw-6rem)] h-[350px]"
                                        layout={{
                                                margin: {b:50, l:60, r:60, t:20},
                                                yaxis: {title: "Base kW Profile"},
                                                legend: {"orientation": "h"}
                                        }}
                                />
                        }
                </div>
        );
}