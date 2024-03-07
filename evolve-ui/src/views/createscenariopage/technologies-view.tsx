import React from 'react';
import { SelectField } from '../../components/select-field';
import { HeaderSection } from './header-section';

interface TechOption {
    id: number;
    name: string;
    displayName: string;
    image: string;
}

export function TechnologiesView(props: any) {

    const { handleChange, technologies } = props;
    const techOptions: TechOption[] = [
        {
            id: 1,
            name: "solar",
            displayName: "Solar",
            image: "./images/solar_icon.svg"
        },
        {
            id: 2,
            name: "ev",
            displayName: "Electric Vehicle",
            image: "./images/ev_icon.svg"
        },
        {
            id: 3,
            name: "energy_storage",
            displayName: "Energy Storage",
            image: "./images/storage_icon.svg"
        }
    ]
    return (
        <React.Fragment>

            <HeaderSection
                title='Select Technologies'
                description='Check the technologies you want 
                to model to see the relevant fields.'
            />

            <div className="flex mb-5 gap-x-5">
                {
                    techOptions.map((techOption: TechOption) => {
                        return (
                            <div key={techOption.id} className='flex items-center'>
                                <SelectField 
                                    name="technologies" 
                                    value={techOption.name} 
                                    onChange={handleChange} 
                                    checked={technologies.includes(techOption.name)} />
                                <img src={techOption.image} width="30" className="mx-3" />
                                <p className='capitalize'> {techOption.displayName} </p>
                            </div>
                        )
                    })
                }
            </div>
        </React.Fragment>
    )
}