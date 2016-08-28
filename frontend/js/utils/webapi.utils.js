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
            request.post(baseUrl + '/accounts/login/')
                .send({username: username, password: password})
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
        return new Promise((resolve, reject) => { resolve() });
    },

    getProfile: function () {
      var promise = new Promise((resolve, reject) => {
          request.post(baseUrl + '/profile/')
              // .send({csrf: getCookie('csrftoken')})
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

    register: function (username, email, password) {
        var promise = new Promise((resolve, reject) => {
            request.post(baseUrl + '/accounts/signup/')
                .send({username: username, password: password, email: email})
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
