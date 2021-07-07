import React from "react"
import Layout from "../components/layout/Layout"
import { showAlert } from "../utils/alert";
import { loginSuccesful } from '../actions/auth';
import { CircularProgress } from "@material-ui/core";

import { authServer } from "../utils/axios";

const Login = () => {
    const [isLoading, setIsLoading] = React.useState(false);
    const [isLogin, setIsLogin] = React.useState(true);
    const [loginData, setLoginData] = React.useState({
        email: '',
        password: ''
    })
    const [signupData, setSignupData] = React.useState({
        name: '',
        email: '',
        password: '',
        confirmPassword: ''
    })
    
    const handleLogin = (e) => {
        e.preventDefault();
        if(isLoading) return
        if(!loginData.email) return showAlert('Email required', 'warning');
        if(!loginData.password) return showAlert('Password required', 'warning');
        setIsLoading(true);
        authServer.post('/login', loginData)
            .then(res => {
                showAlert('Login succesful!', 'success');
                loginSuccesful(res.data.user, res.data.token);
                localStorage.setItem('token', res.data.token);
                window.location.href = "/deconstructor";
            }).catch(err => {
                setIsLoading(false);
                console.log(err);
                if(err.response)
                    return showAlert(err.response.data.message, 'error');
                return showAlert('Internal server error, try again later', 'error');
            })
        console.log(loginData);
    }

    const handleSignup = (e) => {
        e.preventDefault();
        if(isLoading) return
        if(!signupData.email) return showAlert('Email required', 'warning');
        if(!signupData.password) return showAlert('Password required', 'warning');
        if(!signupData.name) return showAlert('Name required', 'warning');
        if(signupData.password !== signupData.confirmPassword) return showAlert('Passwords do not match', 'warning');
        setIsLoading(true);
        authServer.post('/signup', signupData)
            .then(res => {
                showAlert('Succesfully signed up!', 'success');
                setTimeout(() => {
                    window.location.reload();
                }, 1500);
            }).catch(err => {
                setIsLoading(false);
                if(err.response)
                    return showAlert(err.response.data.message, 'error');
                return showAlert('Internal server error, try again later', 'error');
                    
            })
        console.log(signupData);
    }

    const LoginForm = (
        <form onSubmit={handleLogin}>
            <div className="flex-col mb-6">
                <div>
                    <label className="block text-green-800 font-bold mb-2" for="inline-full-name">
                        Email
                    </label>
                </div>
                <div className="w-full">
                    <input 
                        className="appearance-none border-2 rounded-xl w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-green-800" 
                        type="text" 
                        value={loginData.email}
                        onChange={(e) => setLoginData({...loginData, email: e.target.value})}
                    />
                </div>
            </div> 
            <div className="flex-col mb-6">
                <div>
                    <label className="block text-green-800 font-bold mb-2" for="inline-full-name">
                        Password
                    </label>
                </div>
                <div className="w-full">
                    <input 
                        className="appearance-none border-2 rounded-xl w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-green-800" 
                        type="password" 
                        value={loginData.password}
                        onChange={(e) => setLoginData({...loginData, password: e.target.value})}
                    />
                </div>
            </div>
            <div className="flex">
                <div className="flex-grow"></div>
                <button type="submit" className={`px-6 py-3 rounded-xl text-white text-right ${isLoading?'bg-gray-400':'bg-green-600'}`} disabled={isLoading}>
                    Login
                    {
                        isLoading?<CircularProgress className="ml-2" color="success" size={16}/>:null
                    }
                </button>
            </div>
        </form>
    )

    const SignUpForm = (
        <form onSubmit={handleSignup}>
            <div className="flex-col mb-6">
                <div>
                    <label className="block text-green-800 font-bold mb-2" for="inline-full-name">
                        Name
                    </label>
                </div>
                <div className="w-full">
                    <input 
                        className="appearance-none border-2 rounded-xl w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-green-800" 
                        type="text" 
                        value={signupData.name}
                        onChange={(e) => setSignupData({...signupData, name: e.target.value})}
                    />
                </div>
            </div> 
            <div className="flex-col mb-6">
                <div>
                    <label className="block text-green-800 font-bold mb-2" for="inline-full-name">
                        Email
                    </label>
                </div>
                <div className="w-full">
                    <input 
                        className="appearance-none border-2 rounded-xl w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-green-800" 
                        type="text" 
                        value={signupData.email}
                        onChange={(e) => setSignupData({...signupData, email: e.target.value})}
                    />
                </div>
            </div> 
            <div className="flex-col mb-6">
                <div>
                    <label className="block text-green-800 font-bold mb-2" for="inline-full-name">
                        Password
                    </label>
                </div>
                <div className="w-full">
                    <input 
                        className="appearance-none border-2 rounded-xl w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-green-800" 
                        type="password" 
                        value={signupData.password}
                        onChange={(e) => setSignupData({...signupData, password: e.target.value})}
                    />
                </div>
            </div>
            <div className="flex-col mb-6">
                <div>
                    <label className="block text-green-800 font-bold mb-2" for="inline-full-name">
                        Confirm Password
                    </label>
                </div>
                <div className="w-full">
                    <input 
                        className="appearance-none border-2 rounded-xl w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-green-800" 
                        type="password" 
                        value={signupData.confirmPassword}
                        onChange={(e) => setSignupData({...signupData, confirmPassword: e.target.value})}
                    />
                </div>
            </div> 
            <div className="flex">
                <div className="flex-grow"></div>
                <button type="submit" className={`px-6 py-3 rounded-xl text-white text-right ${isLoading?'bg-gray-400':'bg-green-600'}`} disabled={isLoading}>
                    Signup
                    {
                        isLoading?<CircularProgress className="ml-2" color="success" size={16}/>:null
                    }
                </button>
            </div>
        </form>
    )

    return (
        <Layout page="login">
            <div className="w-96 absolute left-1/2 top-1/2 bg-green-200 transform -translate-x-1/2 -translate-y-1/2 rounded-3xl flex-col p-4">
                <div className="flex">
                    <div onClick={() => setIsLogin(true)} className={`mx-3 border-b-2 py-2 cursor-pointer ${isLogin? 'border-green-800': 'border-green-200'}`}>
                        Login
                    </div> 
                    <div onClick={() => setIsLogin(false)} className={`mx-3 border-b-2 py-2 cursor-pointer ${!isLogin? 'border-green-800': 'border-green-200'}`}>
                        Signup
                    </div>                
                </div>
                <div className="mt-6">
                    {isLogin? LoginForm: SignUpForm}
                </div>                            
            </div>
        </Layout>
    )
}

export default Login