import React from 'react';

interface HeaderSectionProps {
    title: string;
    description: string;
};

interface ColoredHeaderSectionProps extends HeaderSectionProps {
    image: string;
}

export const HeaderSection: React.FC<HeaderSectionProps> = ({
    title, description
}) => {
    return (<div className='border-b-2 mb-5'>
        <p className='text-blue-500 font-bold text-xl pb-1 capitalize'> {title} </p>
        <p className='text-gray-500'> {description} </p>
    </div>)
}

export const ColoredHeaderSection: React.FC<ColoredHeaderSectionProps> = ({
    title, description, image
}) => {
    return (
    <div className="bg-blue-500 flex items-center px-2 py-1 gap-x-5">
        <img src={image} width="25" />
        <div className='text-white'>
            <p className="font-bold"> {title} </p>
            <p> {description} </p>
        </div>
    </div>
    )
}