var WebAPI = require('../utils/webapi.utils');
var AuthTypes = require('../constants/socialauth').AUTH_TYPES;

module.exports = {
    logIn: function(username, pass) {
      var promise = new Promise((resolve, reject) => {
        if (localStorage.isLoggedIn) {
            resolve();
        }

        WebAPI.logIn(username, pass).then((res) => {
          //localStorage.token = res.token;
          // localStorage.auth_type = AuthTypes.LOCAL;
          localStorage.isLoggedIn = true;
          resolve();
        }, (err) => {
          reject(err)
        });
      })

      return promise;
    },

    logOut: function() {
      var promise = new Promise((resolve, reject) => {
        WebAPI.logOut(localStorage.auth_type).then(() => {
          // delete localStorage.token;
          // delete localStorage.auth_type;
          delete localStorage.isLoggedIn;
          resolve();
        }, (err) => {
          console.log(err);
          reject();
        })
      });

      return promise;
    },

    loggedIn: function() {
        return !!localStorage.isLoggedIn
    },

    socialLogIn: function (type) {
      switch(type) {
        case AuthTypes.LINKEDIN:
          var promise = new Promise((resolve, reject) => {
            localStorage.token = 'xyz';
            localStorage.auth_type = AuthTypes.LINKEDIN;
            resolve();
          });
          return promise;
      }
    },

    getProfile() {
      return WebAPI.getProfile();
    },

    register(username, email, password) {
      return WebAPI.register(username, email, password);
    }
}
