
const getCheckedItems = (e:any, items: any) => {
        
    if (e.target.checked && !items.includes(e.target.value)) {
        items.push(e.target.value)
    } else if (!e.target.checked && items.includes(e.target.value)){
        items.splice(items.indexOf(e.target.value))
    }

    return items

}

const handleChangeArray = (e: any, id: string, dataArray: any,  setData:any) => {
    
    let data = dataArray.filter((item:any) => item.id === id)
    let name = e.target.name

    if (e.target.type == 'checkbox') {

        if (data[e.target.name] instanceof Array) {
            let items = data[e.target.name];
            items = getCheckedItems(e, items)
            setData((arr:any)=> arr.map((x:any)=> id === x.id ? {
                ...x, [name]: items
            }: x))

        } else {
            let value = e.target.checked
            setData((arr:any)=> arr.map((x:any)=> id === x.id ? {
                ...x, [name]: value
            }: x))
        }

    } else {
       
        let value = e.target.value 
        setData((arr:any)=> arr.map((x:any)=> id === x.id ? {
            ...x, [name]: value
        }: x))
    }
}

const handleChange = (e: any, data: any, setData: any) => {

 
    if (e.target.type == 'checkbox') {

        if (data[e.target.name] instanceof Array) {
            let items = data[e.target.name];
            items = getCheckedItems(e, items)
            setData({...data, 
                [e.target.name]: items})

        } else {
            setData({...data, 
                [e.target.name]: e.target.checked})
        }

    } else {

        setData({...data, 
            [e.target.name]: e.target.value})
    }
    
}

const validateInput = (data:any, schema: any, setErrorFunc: any) => {
    schema.validate(data, { abortEarly: false }).then(
        (value:any)=> {
            setErrorFunc({})
        }
    ).catch((err:any)=> {
        setErrorFunc(err.inner.reduce((result:any, item:any)=> {
            result[item.path] = item.message
            return result
        }, {}))
    })
}

const validateInputArray = (data:any, schema: any, setErrorFunc: any) => {

    data.map((item:any, index:any)=> {
        schema.validate(item, { abortEarly: false }).then(
            (value:any)=> {
                setErrorFunc((arr:any)=> arr.map((x:any, innerIndex: any)=> innerIndex === index ? {}: x))
            }
        ).catch((err:any)=> {
            setErrorFunc(
                (arr:any) => arr.map( (x:any, innerIndex:any) => innerIndex === index ?
                    err.inner.reduce((result:any, el:any)=> {
                    result[el.path] = el.message
                    return result
                    }, {}): x
                )
            )
        })
    })
    
}

export {handleChangeArray, handleChange, validateInput, 
    validateInputArray};