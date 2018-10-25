require('bootstrap-sass');
window.Vue = require('vue');


import client from 'socket.io-client';

const socket = client.connect('http://' + document.domain + ':' + location.port + '/test');

console.log('http://' + document.domain + ':' + location.port);


socket.on('connect', function () {
    console.info('Socket connected !');
});
socket.on('message', function (msg) {
    alert('Got ' + msg);
});

socket.on('disconnect', function () {
    console.info('Socket disconnected');
});
socket.send('Hello');
console.log('Hello');

socket.on('connect', function () {
    console.log('send request to my event');
    socket.emit('my event', {data: 'I\'m connected!'});
});
socket.on('disconnect', function () {
    console.log('Disconnected');
});
socket.on('my response', function (msg) {
    console.log('<br>Received: ' + msg.data);
});


const data = {
    items: [
        '1',
        '12',
        '13',
        '14',
    ]
};

const ItemsComponents = Vue.extend({
    data: () => {return data},
    delimiters: ['{(', ')}'],
    template: `<ul><li v-for="item in items">{(item)}</li></ul>`
});


Vue.component('items-component', ItemsComponents);



new Vue({
    el: '#app',
    data: data
});
// var ws = new WebSocket("ws://localhost:8000/websocket");
// ws.onopen = function() {
//     ws.send("Hello, world");
// };
// ws.onmessage = function (evt) {
//     alert(evt.data);
// };