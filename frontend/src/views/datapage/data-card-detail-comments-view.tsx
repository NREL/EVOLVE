import React from 'react';
import {useSelector} from 'react-redux';
import {StateModel} from "../../interfaces/redux-state";
import { TimeSeriesDataCommentModel } from "../../interfaces/data-manage-interfaces";
import {DataCardDetailCommentsEmptyView} from "./data-card-detail-comments-empty";

export function DataCardDetailCommentsView (props:any) {

    const {comments, editCommentFlag,  setNewComment, handleAddComment,
        handleCommentDelete, setEditCommentFlag, setEditComment, handleEditComment} = props;

   
    const user = useSelector( (state: StateModel) => state.auth.user)

    const getEditCommentView = (c:TimeSeriesDataCommentModel) => {
                                    
            if (editCommentFlag === c.id){

                return  <input type="textarea" name="comment" 
                className="border w-full px-2 h-10 outline-none" 
                key={c.id}
                placeholder={c.comment}
                onChange={(e: React.ChangeEvent<HTMLInputElement>)=> setEditComment(e.target.value)}
                onKeyDown={(e: React.KeyboardEvent<HTMLInputElement>) => handleEditComment(e, c.timeseriesdata_id, c.id)}/>
            } 
            return <p className="pt-2">{c.comment}</p>
            
    }

    return (
        <div>
            <div>
                <h1 className="text-blue-500 font-bold mb-2 border-b-2 w-max"> Comments </h1>
                <p className="text-sm text-gray-500 mb-3"> Manage comments. </p>
                <input type="textarea" name="comment" 
                className="border w-full px-2 h-10 outline-none" placeholder="Enter your comment"
                onChange={(e:React.ChangeEvent<HTMLInputElement>)=> setNewComment(e.target.value)}
                onKeyDown={(e:React.KeyboardEvent<HTMLInputElement>) => handleAddComment(e)}
                />
            </div>

            {
                comments.length >0 ? comments.map((c: TimeSeriesDataCommentModel)=> {
                    return <div className="py-2 border-b">
                        
                        <p className="text-sm"> 
                            <span className={`text-white rounded-md px-1 " + ${(
                                c.username === user
                            )?'bg-blue-500 ':'bg-gray-500'}`} >  
                            {c.username} </span> <span className="pl-1"> commented at {c.updated_at}</span> 
                        </p>
                        
                        {
                            c.username === user && 
                            <div className="flex">
                        
                                <div className="flex justify-center align-center w-6 h-6 hover:cursor-pointer 
                                    hover:bg-gray-300 hover:rounded-full"
                                    onClick={()=> handleCommentDelete(c.timeseriesdata_id, c.id)}>
                                    <img src="./images/delete_light.svg" width="12" className=""/>
                                </div>

                                <div className="flex justify-center align-center w-6 h-6 
                                    hover:cursor-pointer hover:bg-gray-300 hover:rounded-full"
                                    onClick={()=> setEditCommentFlag(c.id)}>
                                    <img src="./images/edit_icon.svg" width="14" className=""/>
                                </div>
                            
                            </div>
                        }
                
                        
                        {getEditCommentView(c)}
                            
                        
                    </div>
                }): <DataCardDetailCommentsEmptyView />
            }
        </div>
    )
    
}