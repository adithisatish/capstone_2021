import axios from 'axios';

const isProduction = process.env.NODE_ENV !== "production"
export const authServer = axios.create({
    baseURL: isProduction? 'https://sentence-deconstructor.herokuapp.com': 'http://localhost:8080'
});
export const decServer = axios.create({
    baseURL: isProduction? 'http://3.108.227.198:5000/': 'http://127.0.0.1:5000/'
});