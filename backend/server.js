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

    let fs = require('fs');
    let obj = JSON.parse(fs.readFileSync('./gamedata.json', 'utf8'));

    let data = obj.data

    let gameSchema = new mongoose.Schema ({
        'teamA' : Array,
        'teamB' : Array,
        'winner': String
    }, {
        writeConcern: {
            w: 'majority',
            j:true,
            wtimeout: 1000
        }
    });


    let Game = mongoose.model('Game', gameSchema, 'game');

    data.forEach((game, _i) => {
        let aGame = new Game({ 'teamA': game['Team A'], 'teamB' : game['Team B'] , 'winner': game['Result']});
        aGame.save(function(err, game){
            console.log('Attempting to write to mongo');
            if (err) return console.log(err);
            console.log('Saved one to game collection');
            console.log(game);
        })
    })

})




app.listen(port, () => {
    console.log(`Server is running on port: ${port}`);
});
