var AuthTypes = require('../constants/socialauth').AUTH_TYPES;
var baseUrl = require('../constants/webapi').BaseUrl;
var request = require('superagent');

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

    getUser: function () {

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
