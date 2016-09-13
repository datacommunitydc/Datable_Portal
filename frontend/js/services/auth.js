var WebAPI = require('../utils/webapi.utils');
var AuthTypes = require('../constants/socialauth').AUTH_TYPES;

module.exports = {
    logIn: function(username, pass) {
      var promise = new Promise((resolve, reject) => {
        if (localStorage.token) {
            resolve();
        }

        WebAPI.logIn(username, pass).then((res) => {
          localStorage.token = res.body.token;
          resolve();
        }, (err) => {
          reject(err)
        });
      })

      return promise;
    },

    logOut: function() {
      var promise = new Promise((resolve, reject) => {
        WebAPI.logOut().then(() => {
          delete localStorage.token;
          resolve();
        }, (err) => {
          reject();
        })
      });

      return promise;
    },

    loggedIn: function() {
        return !!localStorage.token
    },

    socialLogIn: function (provider, accessToken) {
      var promise = new Promise((resolve, reject) => {
        if (localStorage.token) {
            resolve();
        }
        WebAPI.socialLogIn(provider, accessToken).then((res) => {
          localStorage.token = res.body.token;
          resolve(res);
        }, (err) => {
          reject(err)
        });
      })

      return promise;
    },

    getProfile() {
      return WebAPI.getProfile();
    },

    register(firstName, lastName, username, email, password) {
      return WebAPI.register(firstName, lastName, username, email, password);
    },

    getQuestions() {
      return WebAPI.getQuestions();
    }
}
