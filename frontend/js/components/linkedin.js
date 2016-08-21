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
        api_key: SocialConstants.LINKEDIN.CLIENT_ID,
        authorize: true
    });
  },

  render: function() {
    return (
      <script type="in/Login"></script>
    );
  },

  onAuthentication() {
      AuthAction.socialLogIn(SocialConstants.AUTH_TYPES.LINKEDIN).then(() => {
        this.context.router.replace('/');
      });
  }
});

module.exports = linkedin;
    
    // Use the API call wrapper to request the member's basic profile data
    function getProfileData() {
        IN.API.Raw("/people/~").result(onSuccess).error(onError);
    }
