var AuthTypes = require('../constants/socialauth').AUTH_TYPES;
var request = require('superagent');

module.exports = {
    logIn: function (username, password) {
        var promise = new Promise((resolve, reject) => {
            resolve({
                token: 'xyz'
            })
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
    },

    getUser() {

    }
};
