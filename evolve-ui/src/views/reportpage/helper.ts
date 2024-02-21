

export const SortObject = (obj: Record<any, any>) => {

    const days: string[] = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat' ];
    const months: string[] = ['Jan', "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    const hours: string[] = ['12 AM', '01 AM', "02 AM", "03 AM", "04 AM",
        "05 AM", "06 AM", "07 AM", "08 AM", "09 AM", "10 AM", "11 AM", "12 PM",
        "01 PM", "02 PM", "03 PM", "04 PM", "05 PM", "06 PM", "07 PM",
        "08 PM", '09 PM', "10 PM", "11 PM"]

    if (obj && 'category' in obj){
        
        [days, months, hours].forEach(cat => {
            const catIndexes = cat.filter((d)=> obj['category'].includes(
                d)).map((d)=> obj['category'].indexOf(d));
    
            if (catIndexes.length > 0){
                for (let key in obj){
                    obj[key] = catIndexes.map((h:any)=> obj[key][h])
                }
            }
        }); 
        
    }

    return obj
}