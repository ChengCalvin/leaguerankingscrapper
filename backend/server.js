const express = require('express');
const cors = require('cors');
const mongoose = require('mongoose') // help connect everything to mongodb

require('dotenv').config();
const app = express();
const port = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

const uri = process.env.ATLAS_URI;

mongoose.connect(uri, {useNewUrlParser: true, useCreateIndex : true});

const connection = mongoose.connection;
connection.once('open', () => {
    console.log('MongoDB database connection established successfully')

    var fs = require('fs');
    var obj = JSON.parse(fs.readFileSync('./gamedata.json', 'utf8'));

    var gameSchema = new mongoose.Schema ({
        game_data: [{
            Team A:
        }]
    })

    var Game = mongoose.model('Game', gameSchema);

    var game = new Game({

    })

})

app.listen(port, () => {
    console.log(`Server is running on port: ${port}`);
});
