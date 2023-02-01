import React from 'react';
import { BaseLoadTSDataInterface } from '../../interfaces/report-interfaces';
import Plot from 'react-plotly.js';

interface NativeLoadViewProps {
        baseLoad: BaseLoadTSDataInterface | null,
        baseEnergyMetrics: any,
        basePeakPowerMetrics: any,
        netLoad: any,
        netEnergyMetrics: any,
        netPeakPowerMetrics: any
}

export const NativeLoadView: React.FC<NativeLoadViewProps> = ({
        baseLoad, baseEnergyMetrics, basePeakPowerMetrics,
        netLoad, netEnergyMetrics, netPeakPowerMetrics
}) => {

        const baseloadTimeSeriesData = baseLoad?.timestamp.length? { x: baseLoad.timestamp, y: baseLoad.kW,
                        type: 'scatter', mode: 'lines',
                        marker: {color: 'red'}, name: 'Base Load'}: null
        const netloadTimeSeriesData = netLoad?.timestamp.length? {
                        x: netLoad.timestamp,y: netLoad.kW,
                        type: 'scatter',mode: 'lines',
                        marker: {color: 'blue'},name: 'Net Load'}: null
        const loadTimeSeriesData = [baseloadTimeSeriesData, netloadTimeSeriesData].filter((el:any)=> el)

        const energyMetricsData = [
                baseEnergyMetrics?.category.length? {
                        x: baseEnergyMetrics.category,y: baseEnergyMetrics.import_kWh,
                        type: 'bar',name: 'Imported kWh (Base)'
                }: null,
                baseEnergyMetrics?.category.length? {
                        x: baseEnergyMetrics.category,y: baseEnergyMetrics.export_kWh,
                        type: 'bar',name: 'Exported kWh (Base)'
                }: null,
                netEnergyMetrics?.category.length? {
                        x: netEnergyMetrics.category,y: netEnergyMetrics.import_kWh,
                        type: 'bar',name: 'Imported kWh (Net)'
                }: null,
                netEnergyMetrics?.category.length? {
                        x: netEnergyMetrics.category,y: netEnergyMetrics.export_kWh,
                        type: 'bar',name: 'Exported kWh (Net)'
                }: null
        ].filter((el:any)=> el)


        const peakPowerMetricsData = [
                basePeakPowerMetrics?.category.length? {
                        x: basePeakPowerMetrics.category,y: basePeakPowerMetrics.import_peak_kW,
                        type: 'bar', name: 'Imported kW (Base)'
                }: null,
                basePeakPowerMetrics?.category.length? {
                        x: basePeakPowerMetrics.category,y: basePeakPowerMetrics.export_peak_kW,
                        type: 'bar',name: 'Exported kW (Base)'
                }: null,
                netPeakPowerMetrics?.category.length? {
                        x: netPeakPowerMetrics.category,y: netPeakPowerMetrics.import_peak_kW,
                        type: 'bar', name: 'Imported kW (Net)'
                }: null,
                netPeakPowerMetrics?.category.length? {
                        x: netPeakPowerMetrics.category,y: netPeakPowerMetrics.export_peak_kW,
                        type: 'bar',name: 'Exported kW (Net)'
                }: null,
        ].filter((el:any)=> el)



        return (
                <div>
                        <div className="grid grid-cols-2">
                        {
                                energyMetricsData.length >0 ? <Plot
                                        data={energyMetricsData}
                                        layout={{
                                                barmode: 'group',
                                                margin: {b:30, l:60, r:20, t:20},
                                                yaxis: {title: "Energy (kWh)"},
                                                legend: {"orientation": "h"}
                                        }}
                                        className="w-full h-[250px] mb-5 mr-5"
                                />: <div className="w-full h-[250px] mb-5 mr-5
                                        bg-gray-200 animate-pulse flex justify-center items-center">
                                                <div className="w-10 h-20 bg-gray-300 mr-3"></div>
                                                <div className="w-10 h-40 bg-gray-300 mr-3"></div>
                                                <div className="w-10 h-10 bg-gray-300"></div>
                                </div>
                        }
                        {
                                peakPowerMetricsData.length > 0 ? <Plot
                                        data={peakPowerMetricsData}
                                        layout={{
                                                barmode: 'group',
                                                margin: {b:30, l:60, r:20, t:20},
                                                yaxis: {title: "Peak Power (kW)"},
                                                legend: {"orientation": "h"}
                                        }}
                                        className="w-full h-[250px] mb-5"
                                /> : <div className="w-full h-[250px] mb-5
                                bg-gray-200 animate-pulse flex justify-center items-center">
                                        <div className="w-10 h-20 bg-gray-300 mr-3"></div>
                                        <div className="w-10 h-40 bg-gray-300 mr-3"></div>
                                        <div className="w-10 h-10 bg-gray-300"></div>
                                </div>
                        }
                        </div>
                        {

                                loadTimeSeriesData.length >0 ? <Plot
                                        data={loadTimeSeriesData}
                                        className="w-[calc(100vw-6rem)] h-[350px]"
                                        layout={{
                                                margin: {b:50, l:60, r:60, t:20},
                                                yaxis: {title: "Base kW Profile"},
                                                legend: {"orientation": "h"}
                                        }}
                                />: <div className="w-[calc(100vw-6rem)] h-[350px]
                                bg-gray-200 animate-pulse flex justify-center items-center">
                                        <div className="w-10 h-20 bg-gray-300 mr-3"></div>
                                        <div className="w-10 h-40 bg-gray-300 mr-3"></div>
                                        <div className="w-10 h-10 bg-gray-300"></div>
                                </div>
                        }
                </div>
        );
}