
// server.js
'use strict';
const http = require('http');
const server = http.createServer(function (req, res) {
    res.writeHead(200, {'content-type': 'text/plain'});
    console.log(squared(2))
    res.end('Hola Mundo');
});
server.listen(8000);

var Odoo = require('odoo-xmlrpc');


var odoo = new Odoo({
    url: 'https://test-livelink.freyi.es',
    db: 'livelink',
    username: 'produccion',
    password: 'produccion',

});


var odoo = new Odoo({
    url: 'http://localhost',
    port: '9013',
    db: 'o13_liv',
    username: 'admin',
    password: 'admin',

});


odoo.connect(function (err) {
    if (err) { return console.log(err); }
        console.log('Connected to Odoo server.');
        // este es el json de datos que debe mandar en función de cada método
        var inParams = [
            [{
				"imei": "9222222",
				"lastConnection": "11/04/2020 11:25",
			},
			{
				"imei": "9222223",
				"lastConnection": "01/05/2020 11:26",
			}]
		];
        var params = [];
        params.push(inParams);
        odoo.execute_kw('aws.device.history', 'insert_history', params, function (err, value) {
            if (err) { return console.log(err); }
            console.log('Result: ', value);
        });
    });

