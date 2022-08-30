
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
    port: '9031',
    db: 'o13_lnk_20220418',
    username: 'rigo1985@gmail.com',
    password: 'TiOdoo2022',

});


odoo.connect(function (err) {
    if (err) { return console.log(err); }
        console.log('Connected to Odoo server.');
        // este es el json de datos que debe mandar en función de cada método
        var inParams = [
            [{
                'imei': '20220508005',
                'email': 'otra.prueba@gmail.com',
                'date': '2022-05-03',
                
                //'pedido': campo text - S042
                //'servicio'
            },{
                'imei': '20220508006',
                'email': 'pruebas1@gmail.com',
                'date': '2022-05-04',
            }]
      ];
        var params = [];
        params.push(inParams);
        odoo.execute_kw('aws.subscription.history',
            'run_subscription', params, function (err, value) {
            if (err) { return console.log(err); }
            console.log('Result: ', value);
        });
    });
 
