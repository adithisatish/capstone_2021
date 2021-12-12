import axios from 'axios';

const isProduction = process.env.NODE_ENV === "production"
export const authServer = axios.create({
    baseURL: isProduction? '/': 'http://localhost:8080'
});
const isFlaskProduction = process.env.NODE_ENV === "production"
export const decServer = axios.create({
    baseURL: isFlaskProduction? 'http://3.111.6.194:5000/': 'http://127.0.0.1:5000/'
});