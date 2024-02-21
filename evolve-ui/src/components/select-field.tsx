import React from 'react';

export function SelectField({ error ,...props}: any) {

    return (
            <input type="checkbox" {...props} 
                className="w-5 h-5 rounded-md"/>
        
    )

}