
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
    url: 'https://livelink.tiodoo.es',
    db: 'o13_lnk_20220216',
    username: 'admin',
    password: 'admin',

});


var odoo = new Odoo({
    url: 'http://localhost',
    port: '9031',
    db: 'o13_lnk_20220614',
    username: 'rigo1985@gmail.com',
    password: 'TiOdoo2022',

});

odoo.connect(function (err) {
    if (err) { return console.log(err); }
        console.log('Connected to Odoo server.');
        // este es el json de datos que debe mandar en función de cada método
        var inParams = [
            [{
				"keyPcbId": "333331",
				"macid": "92222227",
				"assembledOn": "01/04/2020 11:25",
				"status": "OK",
				"testResult":{
						"ADC":"OK",
						"FLASH":"OK",
						"ACCEL":"OK",
						"INTR":"OK",
						"CARGA":"OK",
						"BT":"OK",
						"scoreADC":10,
						"scoreFLASH":40,
						"scoreACCEL":50,
						"scoreINTR":60,
						"scoreCARGA":70,
						"scoreBT":80,
						"totalScore":90
					},
			},

			{
				"keyPcbId": "433332",
				"assembledOn": "01/04/2020 11:25",
				"macid": "92222228",
				"status": "NOK",
				"testResult":{
						"ADC":"OK",
						"FLASH":"NOK",
						"ACCEL":"OK",
						"INTR":"NOK",
						"CARGA":"OK",
						"BT":"OK",
						"scoreADC":10,
						"scoreFLASH":5,
						"scoreACCEL":50,
						"scoreINTR":5,
						"scoreCARGA":70,
						"scoreBT":1,
						"totalScore":90
					},
			}]
      ];
        var params = [];
        params.push(inParams);
        odoo.execute_kw('aws.key', 'insert_key', params, function (err, value) {
            if (err) { return console.log(err); }
            console.log('Result: ', value);
        });
    });
