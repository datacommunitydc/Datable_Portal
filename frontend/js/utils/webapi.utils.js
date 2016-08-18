var AppAction = require('../actions/action');
var SocialConstants = require('../constants/socialauth.js');
var request = require('superagent');

module.exports = {
    getLinkedinAccessToken: function (code) {
        var clientId = SocialConstants.LINKEDIN.CLIENT_ID,
            clientSecret = SocialConstants.LINKEDIN.CLIENT_SECRET,
            redirect_uri = window.location.origin + '/linkedin-auth'

        request.get('https://www.linkedin.com/oauth/v2/accessToken?grant_type=authorization_code&code='+ code +'&redirect_uri=' + redirect_uri + '' + '&client_id=' + clientId + '&client_secret=' + clientSecret)
            .end(function(err, response) {
                if(err) {
                    console.log(err);
                    return; 
                } 
                
                console.log(response);
            });
    },

    getLinkedinProfile: function (accessToken) {
        console.log(accessToken)
        request.get('https://api.linkedin.com/v1/people/~?oauth2_access_token=' + accessToken + '&format=json')
            .end(function(err, response) {
                if(err) {
                    console.log(err);
                    return; 
                } 
                
                console.log(response);
            });
    }
};
