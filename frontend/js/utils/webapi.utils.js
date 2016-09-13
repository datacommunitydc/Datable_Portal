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
            request.post(baseUrl + '/login/')
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

    socialLogIn: function (provider, accessToken) {
        var promise = new Promise((resolve, reject) => {
            request.post(baseUrl + '/verify-token/')
                .set('Content-Type', 'application/x-www-form-urlencoded')
                .send({
                    provider: provider,
                    access_token: accessToken
                })
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

    logOut: function () {
        return new Promise((resolve, reject) => resolve());
    },

    getProfile: function () {
      var promise = new Promise((resolve, reject) => {
          request.get(baseUrl + '/profile/')
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

    getQuestions: function() {
       var promise = new Promise((resolve, reject) => {
           request.get('questions.json')
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
    }
};
