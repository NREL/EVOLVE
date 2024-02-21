import React from 'react';
import { TransparentBackGroundLayout } from '../../utility/description-layout';
import { DescViewProps } from './desc-interfaces';


export const DataFilingStrategyDesc: React.FC<DescViewProps> = ({
    setCloseView
}) => {

   
    return <TransparentBackGroundLayout setCloseView={setCloseView}>
        <div className='h-[500px] overflow-y-scroll'>
            <h1 className='font-bold pb-1 mb-3 text-xl border-b'> Data Filling Strategy </h1>
            <p> When the data set you selected has coarse time resolution and you want to perform
                simulation in finer resolutions you need to select appropriate data filing strategy. Two 
                strategies are available for you to choose from; linear interpolation and staircase fill.
            </p>

            <p className='py-2'> Linear interpolation as name suggests fills data beween two time points by 
            linearly interpolating data between these points. Staircase fill is a simpler approach where 
            data between two time points remain constant. </p>

            <p> The image below illustrates these two data filing approaches.  </p>

            <img src='./data_filling.png' />
        </div>
    </TransparentBackGroundLayout>
}