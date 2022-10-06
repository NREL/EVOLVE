const loggedReducer = (state = {'user': null, 'accessToken': null}, action) => {
    switch(action.type) {
        case 'SIGN_IN':
            console.log('I am here!', action.payload)
            return action.payload
        default:
            return state;
    }
}

export default loggedReducer;