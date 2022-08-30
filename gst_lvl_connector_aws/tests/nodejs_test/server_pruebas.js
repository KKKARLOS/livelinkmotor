
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
				"testedOn": "01/04/2020 20:59",
				"status": "OK",
				"results":{
							"testCaseId": 1234123214,
							"GPRS": "OK",//NOK
							"FTPS": "OK",//NOK
							"GPS": "OK",//NOK
							"IMU": "OK",//NOK
							"memory": "OK",//NOK
							"battery": "OK",//NOK
							"scoreGPRS": 90,//Score es un numero
							"scoreFTPS": 77,//NOK
							"scoreGPS": 70, //Score es un numero
							"scoreIMU": 45, //Score es un numero
							"scoreMemory": 67, //Score es un numero
							"scoreBattery": 89, //Score es un numero
							"totalScore": 59, //Score es un numero
						}
			},
			{
				"imei": "9222223",
				"testedOn": "01/04/2020 20:59",
				"status": "NOK",
				"results":{
							"testCaseId": 1234123213,
							"GPRS": "OK",//NOK
							"FTPS": "NOK",//NOK
							"GPS": "OK",//NOK
							"IMU": "OK",//NOK
							"memory": "OK",//NOK
							"battery": "OK",//NOK
							"scoreGPRS": 66,//Score es un numero
							"scoreFTPS": 33,//NOK
							"scoreGPS": 83, //Score es un numero
							"scoreIMU": 38, //Score es un numero
							"scoreMemory": 65, //Score es un numero
							"scoreBattery": 55, //Score es un numero
							"totalScore": 83, //Score es un numero
						}
			}]
		];
        var params = [];
        params.push(inParams);
        odoo.execute_kw('aws.device.test', 'insert_device_test', params, function (err, value) {
            if (err) { return console.log(err); }
            console.log('Result: ', value);
        });
    });

