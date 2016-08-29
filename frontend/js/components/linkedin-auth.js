var React = require('react');
var WebAPIUtils = require('../utils/webapi.utils.js');
var SocialConstants = require('../constants/socialauth.js');

function getAccessToken(key) {
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
    debugger;
    var code = getAccessToken('code');
    // if(authToken && window.opener && window.opener.setAccessToken) {
    //     window.opener.setAccessToken(authToken);
    // }
    //window.close();
    if(code) {
        var clientId = SocialConstants.LINKEDIN.CLIENT_ID,
          clientSecret = SocialConstants.LINKEDIN.CLIENT_SECRET,
          redirect_uri = window.location.origin + '/linkedin-auth';

        window.location.href = 'https://www.linkedin.com/oauth/v2/accessToken?grant_type=authorization_code&code=' + code + '&client_id='+ clientId +'&redirect_uri='+ encodeURIComponent(redirect_uri) +'&client_secret=' + clientSecret;
    }
  },

  render: function () {
      return (
          <div></div>
      );
  }
});

module.exports = linkedin;
