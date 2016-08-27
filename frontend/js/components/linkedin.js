var SocialConstants = require('../constants/socialauth.js');
var AuthAction = require('../actions/auth.js');
var React = require('react');

var linkedin = React.createClass({
  contextTypes: {
      router: React.PropTypes.object.isRequired
  },

  componentDidMount: function () {
    //IN.Event.on(IN, "auth", this.onAuthentication);
    IN.init({
        api_key: SocialConstants.LINKEDIN.CLIENT_ID
    });
  },

  render: function() {
    return (
      <button className="icon linkedin" onClick={this.authenticate}><i className="fa fa-linkedin" aria-hidden="true"></i></button>
    );
  },

  authenticate() {
    var self = this;

    IN.User.authorize(function() {
      IN.API.Raw("/people/~:(id,firstName,lastName,emailAddress)?format=json").result(onSuccess).error(onError);
    }, this);

    // Handle the successful return from the API call
    function onSuccess(data) {
      var userData = {
        email: data.emailAddress,
        firstName: data.firstName,
        lastName: data.lastName,
        type: SocialConstants.AUTH_TYPES.LINKEDIN
      }

      AuthAction.socialLogIn(userData).then(() => {
        self.context.router.replace('/');
      })
    }

    // Handle an error response from the API call
    function onError(error) {
        console.log(error);
    }
  }
});

module.exports = linkedin;
