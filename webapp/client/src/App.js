import React  from "react";
import { connect } from 'react-redux';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';

import Login from "./pages/Login";
import Landing from "./pages/Landing";
import Deconstructor from "./pages/Deconstructor";
import NotFound from './pages/NotFound';
import Loading from "./components/layout/Loading";
import AuthenticatedRoute from "./AuthenticatedRoute";

import Alert from "./utils/alert";
import { updateLoading, loginSuccesful } from "./actions/auth";
import { authServer } from "./utils/axios";


const App = (props) => {

	React.useEffect(() => {
		const token = localStorage.getItem('token');
		if(!token) return updateLoading(false);
		const config = {
            headers: {
                'Content-Type': 'application/json',
                'x-auth-token': token,
            },
        };

		authServer.post('/authenticateUser', {}, config)
			.then(res => {
				return loginSuccesful(res.data.user, res.data.token);
			}).catch(err => {
				// localStorage.removeItem('token');
				return updateLoading(false);
			})
  	}, [])

  	if(props.loading) return <Loading/>;

  	return (
    	<Router>
			<Switch>
				<Route exact path='/' component={Landing} />
				<AuthenticatedRoute exact auth={true} path='/deconstructor' component={Deconstructor} />
        		<AuthenticatedRoute exact auth={false} path='/login' component={Login} />
				<AuthenticatedRoute auth={false} component={NotFound} />
			</Switch>
			<Alert></Alert>
		</Router>
  	);
}

const mapStateToProps = (state) => ({
	loggedIn: state.auth.loggedIn,
	loading: state.auth.loading,	
});

export default connect(mapStateToProps)(App);