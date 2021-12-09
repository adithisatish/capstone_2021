const isProduction = process.env.NODE_ENV==="production"
const config = {
    "jwtSecret":process.env.JWT_SECRET,
    "apiKey": process.env.API_KEY,
    "authDomain": process.env.AUTH_DOMAIN,
    "projectId": process.env.PROJECT_ID,
    "storageBucket": process.env.STORAGE_BUCKET,
    "messagingSenderId": process.env.MESSAGING_SENDERID,
    "appId": process.env.APP_ID
}
if(!isProduction){
    const devConfig = require("./dev_config.json")
    for(let key in config){
        config[key] = devConfig[key]
    }
}

module.exports = config