var React = require('react');
var SocialConstants = require('../constants/socialauth');
var request = require('superagent');
var GithubUrl = require('../constants/webapi').GithubUrl;

function getCode(key) {
  var hash = window.location.href;
  if(hash) {
    var startIndex = hash.indexOf(key+ '='),
      lastIndex = hash.indexOf('&', startIndex);

    if(lastIndex === -1) {
        lastIndex = hash.length;
    }

    return startIndex > 0 && lastIndex > 0 ? hash.slice(startIndex + (key + '=').length, lastIndex) : '';
  } else {
    return '';
  }
}

var github = React.createClass({
  componentDidMount: function () {
    var code = getCode('code');
    if(code) {
        var clientId = SocialConstants.GITHUB.CLIENT_ID,
          clientSecret = SocialConstants.GITHUB.CLIENT_SECRET,
          redirect_uri = window.location.origin + '/github-auth',
          state = 'DCEeFWf45A53sdfKef424',
          url = GithubUrl + '/login/oauth/access_token?state='+ state +'&code=' + code + '&client_id='+ clientId +'&redirect_uri='+ encodeURIComponent(redirect_uri) +'&client_secret=' + clientSecret;

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

module.exports = github;
