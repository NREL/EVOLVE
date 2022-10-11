
const tsDataFilterReducer = (state = {
    kwCheck: true, irrCheck: true, timeSort: 'descending'
}, action) => {

    switch(action.type) {
        case 'UPDATE_KW':
            return {
                ...state,
                kwCheck: action.payload
            }

        case 'UPDATE_IRR':
            return {
                ...state,
                irrCheck: action.payload
            }

        default:
            return state;
    }
}

export default tsDataFilterReducer;