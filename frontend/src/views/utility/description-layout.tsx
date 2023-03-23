import React from 'react';
import {AiOutlineCloseCircle} from 'react-icons/ai'

interface BackGroundLayoutProps {
    children: JSX.Element;
    setCloseView: React.Dispatch<React.SetStateAction<boolean>>;
}

export const TransparentBackGroundLayout: React.FC<BackGroundLayoutProps> = (
    {children, setCloseView}
) => {
    return (
        <>
            <div className='bg-gray-900
                fixed top-0 left-0 h-screen w-full
                opacity-95 flex items-center justify-center'>

                <div className='w-2/3 bg-white 
                                px-10 py-5 rounded-md shadow-md relative'>
                    {children}
                    <div className='absolute right-5 top-3'>
                        <AiOutlineCloseCircle size={30} 
                            className="hover:cursor-pointer hover:text-red-500"
                            onClick={()=> setCloseView(true)}
                        />
                    </div>
                </div>
            </div>
        </>
    )
}