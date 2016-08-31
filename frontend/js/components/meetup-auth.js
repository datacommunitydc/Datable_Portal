var React = require('react');
var SocialConstants = require('../constants/socialauth');
var request = require('superagent');
var MeetupUrl = require('../constants/webapi').MeetupUrl; 

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
    var code = getCode('code');
    if(code) {
        var clientId = SocialConstants.MEETUP.KEY,
          clientSecret = SocialConstants.MEETUP.SECRET,
          redirect_uri = window.location.origin + '/meetup-auth', 
          url = MeetupUrl + `/oauth2/access?grant_type=authorization_code&code=${code}&client_id=${clientId}&redirect_uri=${encodeURIComponent(redirect_uri)}&client_secret=${clientSecret}`;

        request.post(url)
        .end((err, res) => {
            if(!err) {
                var authToken = res.body.access_token;
                if(authToken && window.opener && window.opener.setAccessToken) {
                    window.opener.setAccessToken(authToken);
                }
                window.close();
            } else {
                console.log(err, res)
            }
        })
    }
  },

  render: function () {
      return (
          <div></div>
      );
  }
});

module.exports = meetup;
