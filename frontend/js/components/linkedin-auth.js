var React = require('react');
var WebAPIUtils = require('../utils/webapi.utils');
var SocialConstants = require('../constants/socialauth');
var request = require('superagent');
var LinkedinUrl = require('../constants/webapi').LinkedinUrl; 

function getCode(key) {
  var hash = window.location.href;
  if(hash) {
    var startIndex = hash.indexOf(key+ '='),
      lastIndex = hash.indexOf('&', startIndex);

    return startIndex > 0 && lastIndex > 0 ? hash.slice(startIndex + (key + '=').length, lastIndex) : '';
  } else {
    return '';
  }
}

var linkedin = React.createClass({
  componentDidMount: function () {
    var code = getCode('code');
    if(code) {
        var clientId = SocialConstants.LINKEDIN.CLIENT_ID,
          clientSecret = SocialConstants.LINKEDIN.CLIENT_SECRET,
          redirect_uri = window.location.origin + '/linkedin-auth', 
          url = LinkedinUrl + '/oauth/v2/accessToken?grant_type=authorization_code&code=' + code + '&client_id='+ clientId +'&redirect_uri='+ encodeURIComponent(redirect_uri) +'&client_secret=' + clientSecret;

        request.post(url).end((err, res) => {
          var authToken = res.body.access_token;

          if(authToken && window.opener && window.opener.setAccessToken) {
            window.opener.setAccessToken(authToken);
          }

          window.close();
        })
    }
  },

  render: function () {
      return (
          <div></div>
      );
  }
});

module.exports = linkedin;
