import React from 'react';

export function SearchDataView (props:any) {

    const {searchProfiles, setSelectedProfile, setIsClicked,
        setSearchProfiles, } = props;

    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul',
        'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    return (
        <div className=" bg-gray-200 w-full p-3">
            {
                searchProfiles.map((profile: Record<string, any>)=> {
                    let profile_mod = {...profile, 
                        start_date: new Date(profile.start_date),
                        end_date: new Date(profile.end_date),
                        created_at: new Date(profile.created_at)
                    }
                    return (
                    <div className="hover:bg-gray-100 px-2 py-1
                        hover:cursor-pointer rounded-md"
                        onClick={()=> {
                            setSelectedProfile(profile)
                            setIsClicked(true)
                            setSearchProfiles([])
                        }}
                    >
                        <div className='flex justify-between'>
                            <p> {profile.name} <span className="bg-gray-400 px-1 rounded-md text-white text-sm text-center"> {profile.owner} </span> </p>
                            <p> {profile.resolution_min}m</p>
                            <p className="bg-blue-500 rounded-md px-1 text-white"> {profile.category }</p>
                        </div>
                        <div className='flex justify-between'>
                            <p> {profile_mod.start_date.getFullYear()} {months[profile_mod.start_date.getMonth()]} </p>
                            <p> {profile_mod.end_date.getFullYear()} {months[profile_mod.end_date.getMonth()]}</p>
                        </div>
                    </div>
                    )
                    
                })  
            }
        </div>                   
    )
}