import axios from 'axios';

const isProduction = process.env.NODE_ENV==="production"
export const authServer = axios.create({
    baseURL: isProduction? 'https://sentence-deconstructor.herokuapp.com': 'http://localhost:8080'
});