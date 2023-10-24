import { useEffect, useState } from "react"
import axios from 'axios';
import {TimeSeriesDataInfoModel} from "../interfaces/data-manage-interfaces";
import {StateModel} from "../interfaces/redux-state";
import {TimeSeriesDataCommentModel} from "../interfaces/data-manage-interfaces";
import {useSelector} from 'react-redux';
import dateFormat from "dateformat";

const useTimeseriesDataComments = (
    cardData: TimeSeriesDataInfoModel
) => {
    
    const [comments, setComment] = useState<TimeSeriesDataCommentModel[]>([])
    const accessToken = useSelector( (state: StateModel) => state.auth.accessToken)

    const handleFetchComment = (data_id: number) => {
        axios.get(
            `/data/${data_id}/comments`,
            {headers: {'Authorization': 'Bearer ' + accessToken}}
        ).then((response)=> {
            let data_sorted = response.data.sort(
                (
                    a: TimeSeriesDataCommentModel,
                    b: TimeSeriesDataCommentModel
                ) => {
                    return new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime()
                }
            )
            let comments_data = data_sorted.map((d: TimeSeriesDataCommentModel)=> {
                    return {
                        ...d, updated_at: dateFormat(d.updated_at, 
                            "dddd, mmmm dS, yyyy, h:MM:ss TT")
                    }
                })
            setComment(comments_data)

        }).catch((error)=> {
            setComment([])
            console.log(error)
            if (error.response.status === 401) {
                localStorage.removeItem('state')
            }
        })
    }

    const handleCommentDelete = (
        data_id: number, 
        id: number
    ) => {
        axios.delete(
            `/data/${data_id}/comments/${id}`,
            {headers: {'Authorization': 'Bearer ' + accessToken}}
        ).then((response)=> {
            console.log(response.data)
            handleFetchComment(cardData.id)
        }).catch((error)=> {
            setComment([])
            console.log(error)
            if (error.response.status === 401) {
                localStorage.removeItem('state')
            }
        })
    }

    const handleUpdateComment = (
        data_id:number, 
        comment_id:number, 
        edited_comment:string
    ) => {
        
        axios.put(
            `/data/${data_id}/comments/${comment_id}`,
            {"comment": edited_comment},
            {headers: {'Authorization': 'Bearer ' + accessToken}}
        ).then((response)=> {
            console.log(response.data)
            handleFetchComment(cardData.id)
        }).catch((error)=> {
            setComment([])
            console.log(error)
            if (error.response.status === 401) {
                localStorage.removeItem('state')
            }
        })
    }



    const handleInsertComment = (
        data_id: number, 
        comment: string
    ) => {
      
        axios.post(
            `/data/${data_id}/comments`,
            {"comment": comment},
            {headers: {'Authorization': 'Bearer ' + accessToken}}
        ).then((response)=> {
            console.log(response.data)
            handleFetchComment(cardData.id)
        }).catch((error)=> {
            setComment([])
            console.log(error)
            if (error.response.status === 401) {
                localStorage.removeItem('state')
            }
        })
    }

    

    useEffect(()=> {

        if (cardData){
            handleFetchComment(cardData.id)
        }

    }, [cardData])


    return [comments, setComment, handleInsertComment, 
        handleCommentDelete, handleUpdateComment]
}

export {useTimeseriesDataComments};