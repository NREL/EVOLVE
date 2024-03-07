import React from 'react';

export function TextField({ error ,...props}: any) {

    return (
        <div className='w-full'>
            <input {...props} 
                className={`${error ? 'border-2 border-red-500': ''} + " w-full bg-gray-200 px-2 py-1 rounded-md outline-0 focus:outline-0"`}/>
            {error && <p className="text-sm text-red-500">{error}</p>}
        </div>
    )

}