
import loggedReducer from "./is-logged";
import { combineReducers } from "redux";

const rootReducer = combineReducers({
    'auth': loggedReducer
});

export default rootReducer;