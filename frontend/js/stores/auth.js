var Dispatcher = require('../dispatchers/dispatcher');
var EventEmitter = require('events').EventEmitter;
var ActionTypes = require('../constants/actions');
var Auth = require('../services/auth');
var assign = require('object-assign');

var CHANGE_EVENT = 'change';

var AppStore = assign({}, EventEmitter.prototype, {
  loggedIn: function () {
      return Auth.loggedIn();
  },

  emitChange: function() {
    this.emit(CHANGE_EVENT);
  },

  addChangeListener: function(callback) {
    this.on(CHANGE_EVENT, callback);
  },

  getProfile: function() {
    if(this.loggedIn()) {
      return Auth.getProfile();
    }

    return Promise.resolve(null);
  },

  getQuestions: function() {
    if(this.loggedIn()) {
      return Auth.getQuestions();
    }

    return Promise.resolve(null);
  }
});

// Register callback to handle all updates
Dispatcher.register(function(action) {
    switch(action.type) {
        case ActionTypes.LOGGED_IN:
        case ActionTypes.LOGGED_OUT:
            AppStore.emitChange();
            break;
    }
});

module.exports = AppStore;
