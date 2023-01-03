import React from 'react';

const CreateLabelButton = (props: any) => {
    return (
        <div className="flex justify-center bg-blue-500 w-60 h-12 rounded-md m-auto mt-12
            hover:cursor-pointer hover:bg-blue-600">
            <button type="button" className="text-xl text-white font-bold"> Create Label </button>
            <img src="./images/label_icon_light.svg" className="ml-3 w-10"/> 
        </div>
    )
}

export {CreateLabelButton};