import React from "react";
import { TextField } from "../../components/text-field";


export function FormGroupsView(props: any) {
    return (
        <>
            {
                props.formFields.map((item: any) => {
                    return (
                        <div>
                            <p> {item.label} </p>
                            <p className='text-sm text-gray-500 pb-2'>
                                {item.description} </p>
                            <TextField error={item.error} name={item.name}
                                type={item.type} value={item.value}
                                onChange={props.handleChange}
                            />
                        </div>
                    )
                })
            }
        </>
    )
};