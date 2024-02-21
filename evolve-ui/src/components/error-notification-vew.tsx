import React from 'react';

export function ErrorNotification (props: any) {

    const {err_text, setCloseNotification} = props;
    

    return (
        <div className="bg-indigo-200 flex justify-between 
        w-4/5 m-auto rounded-md px-5 py-1 mt-2"> 
            <p className='text-red-500'> {err_text.length < 100 ? err_text: err_text.slice(0,100) + '...' }  </p>
            <p className="hover:bg-indigo-300 w-6 h-6 rounded-full 
                text-center hover:cursor-pointer"
            onClick={()=> setCloseNotification(true)}> X </p>
        </div>
    )
}