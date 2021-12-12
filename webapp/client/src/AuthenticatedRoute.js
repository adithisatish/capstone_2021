import React from 'react';
import { Route, Navigate } from 'react-router-dom';
import { connect } from 'react-redux';

const AuthenticatedRoute = ({loggedIn, component: Component, auth}) => {

    return (                
        ((loggedIn && auth) || !auth) ? <Component /> : <Navigate to="/" />
    );
};

const mapStateToProps = function(state){
    return({
        loggedIn: state.auth.loggedIn
    })
}
export default connect(mapStateToProps)(AuthenticatedRoute);