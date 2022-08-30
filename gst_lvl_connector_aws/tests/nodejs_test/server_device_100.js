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
    db: 'o13_lnk_20220617',
    username: 'rigo1985@gmail.com',
    password: 'TiOdoo2022',
});


odoo.connect(function (err) {
    if (err) { return console.log(err); }
        console.log('Connected to Odoo server.');
        // este es el json de datos que debe mandar en función de cada método

        var _IMEI = []
        var _MAC_ = []
        var i = 0;
        while (i < 100) {
            i = i + 1;
            var add = '0';
            if (i >= 10) {add = '';}
            var imei = '202206160' + add + i.toString();
            _IMEI.push({
                "assembledOn": "16/06/2022 11:25",
				"status": "OK",
				"imei": imei,
				"devicePcbId": "333331",
				"iccid": "9333333",
                'device_test_ids': [[0,0,{'status': 'OK'}]]
			})

            var mac = '202206169' + add + i.toString();
            _MAC_.push({
				"keyPcbId": "333331",
				"macid": mac,
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
					}
			})
            //console.log(i);
            //console.log(add);
        }
        //console.log([miArray]);

        var params = [];
        params.push([_IMEI]);
        odoo.execute_kw('aws.device', 'insert_device', params, function (err, value) {
            if (err) { return console.log('Error: ', err); }
            console.log('Result: ', value);
        });

        var params = [];
        params.push([_MAC_]);
        odoo.execute_kw('aws.key', 'insert_key', params, function (err, value) {
            if (err) { return console.log(err); }
            console.log('Result: ', value);
        });

    });
