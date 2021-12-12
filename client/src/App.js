import React  from "react";
import { connect } from 'react-redux';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';

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
      <React.Fragment>
        <Router>
          <Routes>
            <Route exact path='/' element={<Landing/>} />
            <Route exact path='/deconstructor' element={<AuthenticatedRoute auth={true} component={Deconstructor}/>} />
            <Route exact path='/login' element={<AuthenticatedRoute auth={false} component={Login}/>} />
            <Route auth={false} element={<NotFound/>} />
          </Routes>
        </Router>
        <Alert></Alert>
      </React.Fragment>
  	);
}

const mapStateToProps = (state) => ({
	loggedIn: state.auth.loggedIn,
	loading: state.auth.loading,	
});

export default connect(mapStateToProps)(App);