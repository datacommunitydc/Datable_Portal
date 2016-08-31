var SocialConstants = require('../constants/socialauth.js');
var React = require('react');
var AuthAction = require('../actions/auth');
var BrowserHistory = require('react-router').browserHistory;

var meetup = React.createClass({
  render: function() {
    return (
      <button className='icon meetup' onClick={this.openWindow}>
        <i className="fa fa-calendar-plus-o " aria-hidden="true"></i>
      </button>
    );
  },

  openWindow: function() {
    var clientId = SocialConstants.MEETUP.KEY,
      redirect_uri = window.location.origin + '/meetup-auth',
      state='ABC';

    window.setAccessToken = function (accessToken) {
      if(accessToken) {
        console.log("meetup token: " + accessToken);
      }
    }

    var url = `https://secure.meetup.com/oauth2/authorize?client_id=${clientId}&response_type=code&redirect_uri=${redirect_uri}&state=${state}`;

    window.open(url, '_meetupAuth', 'resizable,scrollbars,status');
  }
});

module.exports = meetup;
