var SocialConstants = require('../constants/socialauth.js');
var React = require('react');
var AuthAction = require('../actions/auth');
var BrowserHistory = require('react-router').browserHistory;

var github = React.createClass({
  render: function() {
    return (
      <button className='icon github' onClick={this.openWindow}>
        <i className="fa fa-github" aria-hidden="true"></i>
      </button>
    );
  },

  openWindow: function() {
    var clientId = SocialConstants.GITHUB.CLIENT_ID,
      redirect_uri = window.location.origin + '/github-auth',
      state = 'DCEeFWf45A53sdfKef424',
      scope = 'user user:email';

    window.setAccessToken = function (accessToken) {
      if(accessToken) {
        AuthAction.socialLogIn(SocialConstants.AUTH_TYPES.GITHUB, accessToken).then(() => {
          BrowserHistory.push('/')
        });
      }
    }

    var url = `https://github.com/login/oauth/authorize?client_id=${clientId}&redirect_uri=${encodeURIComponent(redirect_uri)}&state=${state}&scope=${encodeURIComponent(scope)}`;

    window.open(url, '_githubAuth', 'resizable,scrollbars,status');
  }
});

module.exports = github;
