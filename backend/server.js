const express = require('express');
const cors = require('cors');
const mongoose = require('mongoose') // help connect everything to mongodb

require('dotenv').config();
const app = express();
const port = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

const uri = process.env.ATLAS_URI;
console.log(uri)

mongoose.connect('mongodb+srv://Calvin:Th3amznm4g3@cluster0-j8hrm.mongodb.net/test?retryWrites=true&w=majority', {useNewUrlParser: true, useCreateIndex : true});

const connection = mongoose.connection;
connection.once('open', () => {
    console.log('MongoDB database connection established successfully')
})

app.listen(port, () => {
    console.log(`Server is running on port: ${port}`);
});