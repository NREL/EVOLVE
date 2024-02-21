import React from 'react';

export function DataCardDetailCommentsEmptyView () {
    return (
       <div className="my-5 opacity-95">
           <img src="./images/comments.svg" className="m-auto"/>
           <p className="text-sm text-gray-500 text-center">  To add comment enter
           the comment in the text box and hit enter in the keyboard. </p>
       </div>
    )
}