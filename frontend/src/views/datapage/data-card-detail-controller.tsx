import React, { useState, useEffect, } from "react";
import {SharedUser} from "./shared-user-view";
import fileDownload from 'js-file-download';
import axios from 'axios';
// import React from "react";
import {StateModel} from "../../interfaces/redux-state";
import { TimeSeriesDataInfoModel, TimeSeriesDataCommentModel } from "../../interfaces/data-manage-interfaces";
import {useSelector} from 'react-redux';
import {DataCardDetailView} from './data-card-detail-view';
import {DataCardDetailControlView} from './data-card-detail-controls-view';
import {DataCardDetailCommentsView} from './data-card-detail-comments-view';
import { DataDownloadForm } from "./data-download-form";



function DataCardDetail(props: {
    data: TimeSeriesDataInfoModel;
    setIsClicked: any;
    setcardData: any;
    handleDeleteData: any;
    comments: any;
    handleInsertComment: any;
    handleCommentDelete: any;
    handleUpdateComment: any;
    handleAddSharedUser:any;
    handleDeleteSharedUser: any;
}){

    const {data, setIsClicked, setcardData, handleDeleteData,
         comments, handleInsertComment, handleCommentDelete,
        handleUpdateComment, handleAddSharedUser, handleDeleteSharedUser} = props

    const [deleteLabel, setDeleteLabel] = useState(false)
    const [downloadLabel, setDownloadLabel] =  useState(false)
    const [newComment, setNewComment] = useState('')
    const [editComment, setEditComment] = useState('')
    const [editCommentFlag, setEditCommentFlag] = useState<null | number>(null)
    const accessToken = useSelector( (state: StateModel) => state.auth.accessToken)
    
    const handleAddComment = (e:React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === 'Enter'){
            e.preventDefault();
            if (newComment.length >0){
                handleInsertComment(data.id, newComment)
            } 
        } 
    }

    const handleEditComment = (
        e:React.KeyboardEvent<HTMLInputElement>, 
        data_id: number,
        id: number
    ) => {
        if (e.key === 'Enter'){
            e.preventDefault();
            if (editComment.length >0){
                setEditCommentFlag(null)
                handleUpdateComment(data_id, id, editComment)
            } 
        } 
    }

    const handleClose = () => {
        setIsClicked(false)
        setcardData({})
    }


    // handle file download
    const handleDataDownload = () => {
        axios.get(`/data/${data.id}/file`,
            {headers: {'Authorization': 'Bearer ' + accessToken}}
        ).then((response)=> {
            fileDownload(response.data, `${data.name}.csv`)
        })
    }

   
    return (
        <div className="relative">
            <div className="absolute w-8 h-8 top-0 flex items-center justify-center 
                rounded-full right-0 hover:cursor-pointer hover:bg-gray-300"
                onClick={()=> handleClose()}
                >X 
            </div>
            <div className="px-3 py-3">
                
                <DataCardDetailView data={data} />
                <SharedUser 
                    data={data} 
                    handleAddSharedUser={handleAddSharedUser}
                    handleDeleteSharedUser={handleDeleteSharedUser}
                />
                <DataCardDetailControlView 
                    data={data}
                    deleteLabel={deleteLabel}
                    setDeleteLabel={setDeleteLabel}
                    handleDeleteData={handleDeleteData}
                    downloadLabel={downloadLabel}
                    setDownloadLabel={setDownloadLabel}
                    handleDataDownload={handleDataDownload}
                />
                <DataDownloadForm />
                <DataCardDetailCommentsView
                    comments = {comments}
                    editCommentFlag = {editCommentFlag}
                    setNewComment= {setNewComment} 
                    handleAddComment={handleAddComment}
                    handleCommentDelete={handleCommentDelete}
                    setEditCommentFlag={setEditCommentFlag}
                    setEditComment={setEditComment}
                    handleEditComment={handleEditComment}
                />
                

                </div>
            </div>
    )
}

export default DataCardDetail;
