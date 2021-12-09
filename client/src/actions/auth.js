import { LOGIN_SUCCESS, LOG_OUT, UPDATE_LOADING } from './types';
import store from '../store';

export const loginSuccesful = (user, token) => {
    store.dispatch({
        type: LOGIN_SUCCESS,
        payload: {user, token}
    })
}

export const logout = () => {
    localStorage.removeItem("token")
    store.dispatch({
        type: LOG_OUT
    })
}

export const updateLoading = (state) => {
    store.dispatch({
        type: UPDATE_LOADING,
        payload: state
    })
}