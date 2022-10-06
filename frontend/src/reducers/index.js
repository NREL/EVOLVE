
import loggedReducer from "./isLogged";
import { combineReducers } from "redux";

const rootReducer = combineReducers({
    'auth': loggedReducer
});

export default rootReducer;