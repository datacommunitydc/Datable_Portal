var SocialConstants = require('../constants/socialauth.js');
var React = require('react');
var AuthAction = require('../actions/auth');
var BrowserHistory = require('react-router').browserHistory;

var linkedin = React.createClass({
  render: function() {
    return (
      <button className='icon linkedin' onClick={this.openWindow}>
        <i className="fa fa-linkedin" aria-hidden="true"></i>
      </button>
    );
  },

  openWindow: function() {
    var clientId = SocialConstants.LINKEDIN.CLIENT_ID,
      redirect_uri = window.location.origin + '/linkedin-auth',
      state = 'DCEeFWf45A53sdfKef424';

    window.setAccessToken = function (accessToken) {
      if(accessToken) {
        AuthAction.socialLogIn(SocialConstants.AUTH_TYPES.LINKEDIN, accessToken).then(() => {
          BrowserHistory.push('/')
        });
      }
    }

    var url = 'https://www.linkedin.com/oauth/v2/authorization?response_type=code&client_id='+ clientId +'&redirect_uri='+ encodeURIComponent(redirect_uri) +'&state=' + state;

    window.open(url, '_linkedinAuth', 'resizable,scrollbars,status');
  }
});

module.exports = linkedin;
