
function HomePage(props) {
    let cards = [
        {
            title: "Manage your Data",
            description: "Manage time series data in one place.",
            image: "./images/cloud_upload.svg",
            to: "/data"
        },
        {
            title: "Create Scenarios",
            description: "Manage creation of DER scenarios.",
            image: "./images/create_scenario.svg",
            to: "/"
        },
        {
            title: "Manage Scenarios",
            description: "Edit, view and delete scenarios. ",
            image: "./images/manage_scenario.svg",
            to: "/scenarios"
        },
        {
            title: "Manage Reports",
            description: "Manage scenario reports in one place.",
            image: "./images/manage_report.svg",
            to: "/"
        }
    ]

    

    return (
        <div>
            <h1 class="my-10 text-xl"> Welcome to EVOLVE! </h1>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-y-10 mb-10">
                { 
                    cards.map((card, i) => {
                        return (
                                    <div key={i} class="bg-white shadow-md w-full sm:w-4/5 p-5 text-center
                                        hover:cursor-pointer hover:bg-gray-200"
                                        onClick={()=> {
                                            console.log('this---- ', card.to)
                                            props.navigation(card.to)}}>
                                        <h1 class="text-xl text-blue-500 font-bold"> {card.title} </h1>
                                        <p class="py-3 px-5"> {card.description} </p>
                                        <img src={card.image} class="pt-3 m-auto"/>
                                    </div>
                        )
                    })
                }
            </div>
        </div>
    )
}

export {HomePage};