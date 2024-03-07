import React from 'react';
import { BaseLoadTSDataInterface } from '../../interfaces/report-interfaces';
import Plot from 'react-plotly.js';
import { SortObject } from './helper';

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

        const columnVar =  baseEnergyMetrics && "timestamp" in baseEnergyMetrics ? "timestamp" : "category";
        const baseEnergyMetrics_ = SortObject(baseEnergyMetrics) ;
        const netEnergyMetrics_ = SortObject(netEnergyMetrics);
        const basePeakPowerMetrics_ = SortObject(basePeakPowerMetrics);
        const netPeakPowerMetrics_ = SortObject(netPeakPowerMetrics)

        const baseloadTimeSeriesData = baseLoad?.timestamp.length? { x: baseLoad.timestamp, y: baseLoad.kW,
                        type: 'scatter', mode: 'lines',
                        marker: {color: 'red'}, name: 'Base Load'}: null
        const netloadTimeSeriesData = netLoad?.timestamp.length? {
                        x: netLoad.timestamp,y: netLoad.kW,
                        type: 'scatter',mode: 'lines',
                        marker: {color: 'blue'},name: 'Net Load'}: null
        const loadTimeSeriesData = [baseloadTimeSeriesData, netloadTimeSeriesData].filter((el:any)=> el)


        const energyMetricsData = [
                baseEnergyMetrics_?.[columnVar].length? {
                        x: baseEnergyMetrics_[columnVar],y: baseEnergyMetrics_.import_kWh,
                        type: 'bar',name: 'Imported kWh (Base)'
                }: null,
                baseEnergyMetrics_?.[columnVar].length? {
                        x: baseEnergyMetrics_[columnVar],y: baseEnergyMetrics_.export_kWh,
                        type: 'bar',name: 'Exported kWh (Base)'
                }: null,
                netEnergyMetrics_?.[columnVar].length? {
                        x: netEnergyMetrics_[columnVar],y: netEnergyMetrics_.import_kWh,
                        type: 'bar',name: 'Imported kWh (Net)'
                }: null,
                netEnergyMetrics_?.[columnVar].length? {
                        x: netEnergyMetrics_[columnVar],y: netEnergyMetrics_.export_kWh,
                        type: 'bar',name: 'Exported kWh (Net)'
                }: null
        ].filter((el:any)=> el)


        const peakPowerMetricsData = [
                basePeakPowerMetrics_?.[columnVar].length? {
                        x: basePeakPowerMetrics_[columnVar],y: basePeakPowerMetrics_.import_peak_kW,
                        type: 'bar', name: 'Imported kW (Base)'
                }: null,
                basePeakPowerMetrics_?.[columnVar].length? {
                        x: basePeakPowerMetrics_[columnVar],y: basePeakPowerMetrics_.export_peak_kW,
                        type: 'bar',name: 'Exported kW (Base)'
                }: null,
                netPeakPowerMetrics_?.[columnVar].length? {
                        x: netPeakPowerMetrics_[columnVar],y: netPeakPowerMetrics_.import_peak_kW,
                        type: 'bar', name: 'Imported kW (Net)'
                }: null,
                netPeakPowerMetrics_?.[columnVar].length? {
                        x: netPeakPowerMetrics_[columnVar],y: netPeakPowerMetrics_.export_peak_kW,
                        type: 'bar',name: 'Exported kW (Net)'
                }: null,
        ].filter((el:any)=> el)



        return (
                <div>
                        <p className='text-gray-600 pb-3 '> The first two plots are aggreagted plots and their time axis will dynamically update 
                           depending upon simulation duration. For e.g. if a simulation was ran for a day, it will show 
                           energy and peak power breakdown by hours. If you are running simulation for a week, it will show 
                           peak power breakdown by day. If you are running for a week it will show peak power breakdown by week.
                           If you are running a simulation for a year, it will show energy and power breakdown by month.

                        </p>
                        <div className="grid grid-cols-2 gap-x-3">
                        {
                                energyMetricsData.length >0 ? <Plot
                                        data={energyMetricsData}
                                        layout={{
                                                barmode: 'group',
                                                margin: {b:10, l:60, r:20, t:50},
                                                title: 'Timeseries Aggregated Energy',
                                                yaxis: {title: "Energy (kWh)"},
                                                legend: {"orientation": "h", x: 0, y:-0.2}
                                        }}
                                        className="w-full h-[400px] mb-5 mr-5"
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
                                                title: 'Timeseries Aggregated Peak Power',
                                                margin: {b:10, l:60, r:20, t:50},
                                                yaxis: {title: "Peak Power (kW)"},
                                                legend: {"orientation": "h", x:0, y:-0.2}
                                        }}
                                        className="w-full h-[400px] mb-5"
                                /> : <div className="w-full h-[250px] mb-5
                                bg-gray-200 animate-pulse flex justify-center items-center">
                                        <div className="w-10 h-20 bg-gray-300 mr-3"></div>
                                        <div className="w-10 h-40 bg-gray-300 mr-3"></div>
                                        <div className="w-10 h-10 bg-gray-300"></div>
                                </div>
                        }
                        
                        </div>
                        <p className='text-gray-600 pb-3'> This plot shows comparison between new loads (after adding DER's to base load profile) vs base loads. The number of data points 
                                shown is limited to 2000 data points for each line. If your simulation has more data points, feel free to download results 
                                and visualize them using excel or other tools of your choice.
                        </p>
                        {

                                loadTimeSeriesData.length >0 ? <Plot
                                        data={loadTimeSeriesData}
                                        className="w-full h-[350px]"
                                        layout={{
                                                margin: {b:50, l:60, r:60, t:50},
                                                yaxis: {title: "Base kW Profile"},
                                                title: "Time Series Power Profile before and after adding DER's",
                                                legend: {"orientation": "h", x:0, y:-0.2}
                                        }}
                                />: <div className="w-full h-[350px]
                                bg-gray-200 animate-pulse flex justify-center items-center">
                                        <div className="w-10 h-20 bg-gray-300 mr-3"></div>
                                        <div className="w-10 h-40 bg-gray-300 mr-3"></div>
                                        <div className="w-10 h-10 bg-gray-300"></div>
                                </div>
                        }
                </div>
        );
}