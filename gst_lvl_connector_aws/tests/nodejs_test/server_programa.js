
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
				"imei": "9222223",
				"fwVersion": "12.3",
				"mtype": "OK",
			}]
		];
        var params = [];
        params.push(inParams);
        odoo.execute_kw('aws.firmware', 'insert_firmware', params, function (err, value) {
            if (err) { return console.log(err); }
            console.log('Result: ', value);
        });
    });

