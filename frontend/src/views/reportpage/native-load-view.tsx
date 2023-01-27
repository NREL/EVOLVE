import React from 'react';
import { BaseLoadTSDataInterface } from '../../interfaces/report-interfaces';
import Plot from 'react-plotly.js';

interface NativeLoadViewProps {
        baseLoad: BaseLoadTSDataInterface | null,
        baseEnergyMetrics: any,
        basePeakPowerMetrics: any
}

export const NativeLoadView: React.FC<NativeLoadViewProps> = ({
        baseLoad, baseEnergyMetrics, basePeakPowerMetrics
}) => {
        return (
                <div>
                        <div className="grid grid-cols-2">
                        {
                                baseEnergyMetrics && baseEnergyMetrics.category.length > 0 &&
                                <Plot
                                data={[
                                {
                                        x: baseEnergyMetrics.category,
                                        y: baseEnergyMetrics.import_kWh,
                                        type: 'bar',
                                        name: 'Imported kWh'
                                },
                                {
                                        x: baseEnergyMetrics.category,
                                        y: baseEnergyMetrics.export_kWh,
                                        type: 'bar',
                                        name: 'Exported kWh'
                                },
                                ]}
                                layout={
                                        {
                                        barmode: 'group',
                                        margin: {b:30, l:60, r:20, t:20},
                                        yaxis: {
                                                title: "Energy (kWh)"
                                        }
                                        }
                                }
                                className="w-full h-[250px] mb-5 mr-5"
                                />
                        }
                        {
                                basePeakPowerMetrics && basePeakPowerMetrics.category.length > 0 &&
                                <Plot
                                data={[
                                {
                                        x: basePeakPowerMetrics.category,
                                        y: basePeakPowerMetrics.import_peak_kW,
                                        type: 'bar',
                                        name: 'Imported kW'
                                },
                                {
                                        x: basePeakPowerMetrics.category,
                                        y: basePeakPowerMetrics.export_peak_kW,
                                        type: 'bar',
                                        name: 'Exported kW'
                                },
                                ]}
                                layout={
                                        {
                                        barmode: 'group',
                                        margin: {b:30, l:60, r:20, t:20},
                                        yaxis: {
                                                title: "Peak Power (kW)"
                                        }
                                        }
                                }
                                className="w-full h-[250px] mb-5"
                                />
                        }
                        </div>
                        {
                                baseLoad && baseLoad.kW.length > 0 &&
                                <Plot
                                data={[
                                {
                                        x: baseLoad.timestamp,
                                        y: baseLoad.kW,
                                        type: 'scatter',
                                        mode: 'lines+markers',
                                        marker: {color: 'red'},
                                },
                                ]}
                                className="w-[calc(100vw-6rem)] h-[350px]"
                                layout={{margin: {b:50, l:60, r:60, t:20},
                                        yaxis: {
                                        title: "Base kW Profile"
                                }
                                }}
                                />
                        }
                </div>
        );
}