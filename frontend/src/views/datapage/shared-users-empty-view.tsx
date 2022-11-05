import React from 'react';

export function ShardUsersEmptyView () {
    return (
       <div className="my-3 opacity-95">
           <img src="./images/share_users.svg" className="m-auto"/>
           <p className="text-sm text-gray-500 text-center"> This data has not been shared with other users yet.</p>
       </div>
    )
}