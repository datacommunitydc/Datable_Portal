var AppDispatcher = require('../dispatchers/dispatcher');
var EventEmitter = require('events').EventEmitter;
var assign = require('object-assign');

var AppStore = assign({}, EventEmitter.prototype, {
});

// Register callback to handle all updates
AppDispatcher.register(function(action) {
});

module.exports = AppStore;
