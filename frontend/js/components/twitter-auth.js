var React = require('react');
var SocialConstants = require('../constants/socialauth');
var request = require('superagent');
var TwitterUrl = require('../constants/webapi').TwitterUrl;

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

var meetup = React.createClass({
  componentDidMount: function () {
    var authToken = getCode('oauth_token');
    if(authToken) {
        window.opener.setAccessToken(authToken);
        window.close();
    }
  },

  render: function () {
      return (
          <div></div>
      );
  }
});

module.exports = meetup;
