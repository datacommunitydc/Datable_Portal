var SocialConstants = require('../constants/socialauth.js');
var React = require('react');
var AuthAction = require('../actions/auth');
var BrowserHistory = require('react-router').browserHistory;
var request = require('superagent');
var TwitterUrl = require('../constants/webapi').TwitterUrl
var oauth = require("oauth");

function getOauth(str, key) {
  var hash = str;
  if(hash) {
    var startIndex = hash.indexOf(key+ '='),
      lastIndex = hash.indexOf('&', startIndex);

    if(lastIndex === -1) {
        lastIndex = hash.length;
    }

    return startIndex >= 0 && lastIndex > 0 ? hash.slice(startIndex + (key + '=').length, lastIndex) : '';
  } else {
    return '';
  }
}

var twitter = React.createClass({
  render: function() {
    return (
      <button className='icon twitter' onClick={this.openWindow}>
        <i className="fa fa-twitter" aria-hidden="true"></i>
      </button>
    );
  },

  openWindow: function() {
    var clientId = SocialConstants.TWITTER.KEY,
      redirectUri = window.location.origin + '/twitter-auth',
      clientSecret = SocialConstants.TWITTER.SECRET,
      accessToken = SocialConstants.TWITTER.ACCESS_TOKEN ;

    request.post(TwitterUrl +'/oauth/request_token')
        .set('Authorization', `OAuth oauth_consumer_key=${clientId}, oauth_nonce="8a5c471ee91d0bbdb8bf7deedbed1d78", oauth_signature="IPMEmbl9aCWD1rzDvxlZa1i8UPU%3D", oauth_signature_method="HMAC-SHA1", oauth_timestamp="1472930539", oauth_token=${accessToken}, oauth_version="1.0"`)
        .end((err ,res) => {
            if(!err) {
              var oauthToken  = getOauth(res.text, 'oauth_token');
              var url = `https://api.twitter.com/oauth/authenticate?oauth_token=${oauthToken}`;
              window.open(url, '_twitterAuth', 'resizable,scrollbars,status');
            }
        });

    window.setAccessToken = function (token) {
      if(token) {
        AuthAction.socialLogIn(SocialConstants.AUTH_TYPES.TWITTER, token).then(() => {
          BrowserHistory.push('/')
        });
      }
    }
  }
});

module.exports = twitter;
