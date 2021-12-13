import axios from 'axios';

const isProduction = process.env.NODE_ENV === "production"
export const authServer = axios.create({
    baseURL: isProduction? '/': 'http://localhost:8080'
});
const isFlaskProduction = process.env.NODE_ENV === "production"
export const decServer = axios.create({
    baseURL: isFlaskProduction? '/proxy': 'http://localhost:5000/deconstructor'
});