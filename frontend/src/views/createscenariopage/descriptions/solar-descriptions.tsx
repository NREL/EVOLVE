import React from 'react';
import { TransparentBackGroundLayout } from '../../utility/description-layout';

interface DescViewProps {
    setCloseView: React.Dispatch<React.SetStateAction<boolean>>
}

export const TiltDescriptionView: React.FC<DescViewProps> = ({
    setCloseView
}) => {

    const data = [
        ['4/12', 18.4],
        ['5/12', 22.6],
        ['6/12', 26.6],
        ['7/12', 30.3],
        ['8/12', 33.7],
        ['9/12', 36.9],
        ['10/12', 39.8],
        ['11/12', 42.5],
        ['12/12', 45.0]
    ]

    return <TransparentBackGroundLayout setCloseView={setCloseView}>
        <>
            <h1 className='font-bold pb-1 mb-3 text-xl border-b'> Tilt (Deg) </h1>
            <p> The tilt angle is the angle from horizontal of the photovoltaic modules 
                in the array. For a fixed array, the tilt angle is the angle from 
                horizontal of the array where 0° = horizontal, and 90° = vertical. 
                For arrays with one-axis tracking, the tilt angle is the angle from 
                horizontal of the tracking axis. The tilt angle does not apply 
                to arrays with two-axis tracking.</p>

            <p className='pt-2'> For an array installed on a building's roof, you may want to choose 
            a tilt angle equal to the roof pitch. Use the table below to convert
            roof pitch in ratio of rise (vertical) over run (horizontal) to tilt angle.</p>

            <table className='table-fixed w-full text-left mt-3'>
                <thead>
                    <tr className='border-b'>
                        <th> Roof pitch (rise/run)</th>
                        <th> Tilt Angle (deg)</th>
                    </tr>
                </thead>
                <tbody>
                    {data.map((item:any)=> {
                        return <tr className='border-b'>
                            {item.map((val:any)=> <td> {val} </td>)}
                        </tr>
                    })}
                </tbody>
            </table>
        </>
    </TransparentBackGroundLayout>
}

export const AzimuthDescriptionView: React.FC<DescViewProps> = ({
    setCloseView
}) => {

    const data = [
        ['N', 0],
        ['NE', 45],
        ['E', 90],
        ['SE', 135],
        ['S', 180],
        ['SW', 225],
        ['W', 270],
        ['NW', 315],
    ]

    return <TransparentBackGroundLayout setCloseView={setCloseView}>
        <div className='h-[500px] overflow-y-scroll'>
            <h1 className='font-bold pb-1 mb-3 text-xl border-b'> Azimuth (Deg) </h1>
            <p> For a fixed array, the azimuth angle is the angle clockwise from true north describing 
                the direction that the array faces. An azimuth angle of 180° is for a south-facing array, 
                and an azimuth angle of zero degrees is for a north-facing array. </p>

            <p> For an array with one-axis tracking, the azimuth angle is the angle clockwise from true 
                north of the axis of rotation. The azimuth angle does not apply to arrays with two-axis tracking. </p>

            <p> The default value is an azimuth angle of 180° (south-facing) for locations in the 
                northern hemisphere and 0° (north-facing) for locations in the southern hemisphere. 
                These values typically maximize electricity production over the year, although local 
                weather patterns may cause the optimal azimuth angle to be slightly more or less than 
                the default values. For the northern hemisphere, increasing the azimuth angle favors 
                afternoon energy production, and decreasing the azimuth angle favors morning energy production. 
                The opposite is true for the southern hemisphere.</p>

            <img src='./azimuth.png' />

            <table className='table-fixed w-full text-left mt-3'>
                <thead>
                    <tr className='border-b'>
                        <th> Heading</th>
                        <th> Azimuth Angle (deg)</th>
                    </tr>
                </thead>
                <tbody>
                    {data.map((item:any)=> {
                        return <tr className='border-b'>
                            {item.map((val:any)=> <td> {val} </td>)}
                        </tr>
                    })}
                </tbody>
            </table>
        </div>
    </TransparentBackGroundLayout>
}

export const SolarModelingAssumptionView: React.FC<DescViewProps> = ({
    setCloseView
}) => {

    const data = [
        ['System Losses', '........'],
        ['Max Tilt', '........'],
        ['Inverter Temperature', '........'],
        ['Temperature Coefficients', '........'],
    ]

    return <TransparentBackGroundLayout setCloseView={setCloseView}>
        <>
            <h1 className='font-bold pb-1 mb-3 text-xl border-b'> Solar Modeling Assumptions </h1>
            <p> EVOLVE uses pvlib library to generate time series solar generation profile. Here are some of the 
                parameters assumed in the model when you are using EVOLVE UI.  Please visit the link below 
                to know more about mathematical equations used to model pv systems.

                <a href='https://pvlib-python.readthedocs.io/en/stable/reference/generated/pvlib.irradiance.get_total_irradiance.html?highlight=get_total_irradiance' className='text-blue-500 underline italic'> https://pvlib-python.readthedocs.io/en/stable/reference/generated/pvlib.irradiance.get_total_irradiance.html?highlight=get_total_irradiance </a>
                
                </p>

            {/* <table className='table-fixed w-full text-left mt-3'>
                <thead>
                    <tr className='border-b'>
                        <th> Heading</th>
                        <th> Parameters </th>
                    </tr>
                </thead>
                <tbody>
                    {data.map((item:any)=> {
                        return <tr className='border-b'>
                            {item.map((val:any)=> <td> {val} </td>)}
                        </tr>
                    })}
                </tbody>
            </table> */}
        </>
    </TransparentBackGroundLayout>
}