var AuthTypes = require('../constants/socialauth').AUTH_TYPES;
var baseUrl = require('../constants/webapi').BaseUrl;
var request = require('superagent');

function getCookie(cname) {
    var name = cname + "=";
    var ca = document.cookie.split(';');
    for(var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

module.exports = {
    logIn: function (username, password) {
        var promise = new Promise((resolve, reject) => {
            request.post(baseUrl + '/api-token-auth/')
                .send({username: username, password: password})
                .end(function(err, res){
                    if (err || !res.ok) {
                        reject(err);
                    } else {
                        resolve(res);
                    }
                });
        });

        return promise;
    },

    socialLogIn: function (data) {
        var promise = new Promise((resolve, reject) => {
            request.post(baseUrl + '/accounts/social-login/')
                .send(data)
                .end(function(err, res){
                    if (err || !res.ok) {
                        reject();
                    } else {
                        resolve();
                    }
                });
        });

        return promise;
    },

    logOut: function (type) {
        switch (type) {
            case AuthTypes.LOCAL:
                return new Promise((resolve, reject) => { resolve() });
            case AuthTypes.LINKEDIN:
                return new Promise((resolve, reject) => {
                    IN.User.logout();
                    resolve();
                });
            default:
                break;
        }

        return new Promise((resolve, reject) => reject());
    },

    getProfile: function () {
      var promise = new Promise((resolve, reject) => {
          request.post(baseUrl + '/profile/')
              .set('Authorization', 'Token ' + localStorage.token )
              .end(function(err, res){
                  if (err || !res.ok) {
                      reject();
                  } else {
                      resolve(res);
                  }
              });
      });

      return promise;
    },

    register: function (firstName, lastName, username, email, password) {
        var promise = new Promise((resolve, reject) => {
            request.post(baseUrl + '/signup/')
                .send({username: username, password: password, email: email, first_name: firstName, last_name: lastName})
                .end(function(err, res){
                    if (err || !res.ok) {
                        reject();
                    } else {
                        resolve();
                    }
                });
        });

        return promise;
    },
};
