

function ScenarioHoverCard () {

    let data = [
        {
            "label": "Add label",
            "icon": "./images/add_icon.svg"
        },
        {
            "label": "Remove label",
            "icon": "./images/delete_icon.svg"
        },
        {
            "label": "View metadaa",
            "icon": "./images/view_icon.svg"
        },
        {
            "label": "Edit metadata",
            "icon": "./images/edit_icon.svg"
        },
        {
            "label": "Delete scenario",
            "icon": "./images/delete_icon.svg"
        }
    ]

    return (
        <div class="bg-gray-300 py-3 px-5 hover:cursor-pointer">
            {
                data.map((d, i)=> {
                    return (
                        <div class="flex items-center mb-2 px-2 py-1 hover:bg-gray-400 hover:rounded-md" key={i}>
                            <img src={d.icon} width="20"/>
                            <p class="pl-3 font-bold"> {d.label}</p>
                        </div>
                    )
                })
            }
        </div>
    )
}

export {ScenarioHoverCard}