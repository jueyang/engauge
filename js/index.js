/*
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 */

// TODO router
var app = {
    // Application Constructor
    initialize: function() {
        this.bindEvents();
    },
    // Bind Event Listeners
    //
    // Bind any events that are required on startup. Common events are:
    // 'load', 'deviceready', 'offline', and 'online'.
    bindEvents: function() {
        document.addEventListener('deviceready', this.onDeviceReady, false);
    },
    // deviceready Event Handler
    //
    // The scope of 'this' is the event. In order to call the 'receivedEvent'
    // function, we must explicitly call 'app.receivedEvent(...);'
    onDeviceReady: function() {
        app.receivedEvent('deviceready');
    },
    // Update DOM on a Received Event
    receivedEvent: function(id) {
        var parentElement = document.getElementById(id);
        var listeningElement = parentElement.querySelector('.listening');
        var receivedElement = parentElement.querySelector('.received');

        listeningElement.setAttribute('style', 'display:none;');
        receivedElement.setAttribute('style', 'display:block;');

        console.log('Received Event: ' + id);
    },
    changeScreen: function() {
        // select the anchor clicked on
        // go to the parent screen, fadeout
        // go to the next screen, fadein
    },
    onSignin: function() {
        // get category list from the server
        var request = new XMLHttpRequest();
        request.open('GET', '../temp-cat.json', true);

        request.onload = function(error) {
            if (request.status >= 200 && request.status < 400) {
                // Success
                var data = JSON.parse(request.responseText),
                    categoryList = document.getElementById('category-list'),
                    text, checkbox, item;

                // populate buttons based on JSON
                for (var i = 0; i < data.length; i ++) {
                    // checkbox
                    checkbox = document.createElement('input');
                    checkbox.type = 'checkbox';
                    checkbox.value = data[i].id;

                    // text
                    text = document.createTextNode(data[i].name);

                    // button
                    item = document.createElement('li');
                    item.className = 'category';
                    item.id = data[i].name; // category name
                    item.appendChild(checkbox);
                    item.appendChild(text);

                    // botton list
                    categoryList.appendChild(item);
                }

            } else {
                console.log(request.status);
            }
        };

        request.onerror = function() {};

        request.send();
    },
    onSubscribe: function() {
        var inputs = document.getElementsByTagName('input'),
            outputs = [];

        // get the checked boxes
        for (i = 0; i < inputs.length; i++) {

            if (inputs[i].type === 'checkbox'){

                var output = {};
                output.id = inputs[i].value;

                if (inputs[i].checked === true) {
                    output.subscribed = 1
                } else {
                    output.subscribed = 0
                }

                outputs.push(output)
            }

        }

        var request = new XMLHttpRequest();

        request.open('POST', '/', true); // url will be replaced by the server ping

        request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
        request.send(outputs);
    }
};

app.initialize();