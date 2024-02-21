import React from 'react';
import { TransparentBackGroundLayout } from '../../utility/description-layout';
import { DescViewProps } from './desc-interfaces';

export const ESStrategyDescView: React.FC<DescViewProps> = ({
    setCloseView
}) => {

    
    return <TransparentBackGroundLayout setCloseView={setCloseView}>
        <>
            <h1 className="font-bold mb-3 border-b-2 w-max"> What is Self Consumption ?</h1>

            <p> During the day when your solar panel is generating more electricty than you are consuming,
                excess generation get's stored in energy storage. The rate of charging is determined by how much energy 
                is needed to fully charge the battery, how much excess power is availble from solar and the maximum power 
                capacity of the battery. The battery get's discharged automatically when solar generation falls below your 
                consumption and discharge rate is determined based on how much energy is available in the battery, 
                how much power your appliances need after subtracting solar power and maximum power rating of the 
                battery. Note the charging rate and discharging rate values are not utilized when self consumption 
                strategy is selected.
            </p>

            <h1 className="font-bold my-3 border-b-2 w-max"> What is Peak Shaving ?</h1>

            <p> Energy storage can be used for peak shaving. In this strategy, the battery is discharged when 
                the load exceeds the certain percentage of peak load e.g. 80% and the rate of discharge is determined based on 
                how much energy is available in the battery, excess load power that needs to be met by the battery, and 
                maximum power capacity of the battery. The battery is charged when load falls below a certian threshold let's say 20% 
                and the rate of the charge is determined based on how much energy is needed to fully charge the battery and 
                maximum power capacity of the battery. 
            </p>
        </>
    </TransparentBackGroundLayout>
}
