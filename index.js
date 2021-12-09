const firebase = require('firebase/app')
require("firebase/firestore");

const express = require('express');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');
const config = require('config');

const cors = require('cors');

const app = express();

app.use(express.json());
app.use(cors());

const firebaseConfig = {
    apiKey: config.get("apiKey"),
    authDomain: config.get("authDomain"),
    projectId: config.get("projectId"),
    storageBucket: config.get("storageBucket"),
    messagingSenderId: config.get("messagingSenderId"),
    appId: config.get("appId")
};

firebase.initializeApp(firebaseConfig);
const db = firebase.firestore();

if(process.env.NODE_ENV === "production"){
    app.use(express.static(path.join(__dirname, "client/build")))
}

app.post('/signup', async (req, res) => {
    try {
        const { name, email, password, confirmPassword } = req.body;
        if(!name) return res.status(400).json({message: 'Name required'});
        if(!email) return res.status(400).json({message: 'Email required'});
        if(password !== confirmPassword) return res.status(400).json({message: 'Passwords do not match'});

        const existingUser = await db.collection('users').where('email', '==', email).get();
        if(!existingUser.empty) return res.status(400).json({'message': 'This email has already been registered'});
        
        const salt = await bcrypt.genSalt(10);
        const hash = await bcrypt.hash(password, salt);
        const user = { name, email, password: hash };
        
        const userRef = await db.collection('users').add(user);
            
        return res.status(200).json({message: 'Succesfully signed up!'});
    } catch(err) {
        console.log(err);
        return res.status(500).json({message: 'Internal server error'});
    }
    
})

app.post('/login', async (req, res) => {
    try {
        const { email, password } = req.body;
        if(!email) return res.status(400).json({message: 'Email required'});
        if(!password) return res.status(400).json({message: 'Password required'});
        const existingUser = await db.collection('users').where('email', '==', email).get();

        if(existingUser.empty) return res.status(400).json({message: 'Account does not exist. Please signup instead.'});

        const user = existingUser.docs.map(doc => ({ ...doc.data(), id: doc.id }))[0];
        
        const isPasswordRight = await bcrypt.compare(password, user.password);
        if(!isPasswordRight) return res.status(400).json({message: 'Incorrect password, please try again'});

        delete user.password;

        const payload = {
			id: user.id + user.id,
			iat: new Date().getTime()
		};

        jwt.sign(payload, config.get('jwtSecret'), (err, token) => {
			if (err) throw err;
			res.status(200).json({
				token,
				user
			});
		});

    } catch(err) {
        console.log(err);
    }
})

app.post('/authenticateUser', async (req, res) => {
	try {
        const token = req.header('x-auth-token');
        const decoded = jwt.verify(token, config.get('jwtSecret'));
		userId = decoded.id.slice(0, decoded.id.length / 2);

		const existingUser = await db.collection('users').doc(userId).get();
		if(!existingUser.exists) return res.status(403).json({ message: 'Invalid token'});
		
        const user = existingUser.data();
        delete user.password;
        
        return res.status(200).json({
			token: req.header('x-auth-token'),
			user
		});
	} catch(err) {
        console.log(err);
		return res.status(500).json({
			message: 'Internal server error'
		});
	}
});


const PORT = process.env.PORT || 8080;

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
})