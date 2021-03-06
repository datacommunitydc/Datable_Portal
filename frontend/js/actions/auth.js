var Dispatcher = require('../dispatchers/dispatcher');
var ActionTypes = require('../constants/actions');
var Auth = require('../services/auth');

module.exports = {
  loggedIn: function(states) {
    Dispatcher.dispatch({
        type: ActionTypes.LOGGED_IN,
        data: true
    });
  },

  loggedOut: function(cities) {
    Dispatcher.dispatch({
        type: ActionTypes.LOGGED_OUT,
        data: false
    });
  },

  logIn: function(username, password) {
    var promise = new Promise((resolve, reject) => {
        Auth.logIn(username, password).then(() => {
            this.loggedIn();
            resolve();
        }, () => { reject() });
    });

    return promise;
  },

  socialLogIn: function (provider, accessToken) {
    var promise = new Promise((resolve, reject) => {
        Auth.socialLogIn(provider, accessToken).then(() => {
            this.loggedIn();
            resolve();
        }, () => { reject() });
    });

    return promise;
  },

  logOut: function(state) {
    var promise = new Promise((resolve, reject) => {
        Auth.logOut().then(() => {
            this.loggedOut();
            resolve();
        }, () => { reject() });
    });

    return promise;
  },

  register: function(firstName, lastName, username, email, password) {
    var promise = new Promise((resolve, reject) => {
        Auth.register(firstName, lastName, username, email, password).then(() => {
            resolve();
        }, () => { reject() });
    });

    return promise;
  },

  getProfile() {
    return Auth.getProfile();
  },
}
