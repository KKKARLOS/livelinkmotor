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
    url: 'https://livelink.tiodoo.es',
    db: 'o13_lnk_20220216',
    username: 'admin',
    password: 'admin',
});


// var odoo = new Odoo({
//     url: 'http://localhost',
//     port: '9031',
//     db: 'o13_lnk_20220321',
//     username: 'admin',
//     password: 'admin',

// });


odoo.connect(function (err) {
    if (err) { return console.log(err); }
        console.log('Connected to Odoo server.');
        // este es el json de datos que debe mandar en función de cada método
        var inParams = [
            [{
				"assembledOn": "01/04/2020 11:25",
				"status": "OK",
				"imei": "292227001",
				"devicePcbId": "333331",
				"iccid": "9333333",
			},

			{
				"devicePcbId": "433332",
				"imei": "292227002",
				"iccid": "9333334",
				"assembledOn": "01/04/2020 11:26",
				"status": "NOK"
			},
			
			{"assembledOn":"14/05/2020 10:41","status":"OK","imei":"292227003","devicePcbId":"6464646","iccid":"6465464646"},
			]
      ];
        var params = [];
        params.push(inParams);
        odoo.execute_kw('aws.device', 'insert_device', params, function (err, value) {
            if (err) { return console.log('Error: ', err); }
            console.log('Result: ', value);
        });
    });
