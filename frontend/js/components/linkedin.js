var SocialConstants = require('../constants/socialauth.js');
var WebAPIUtils = require('../utils/webapi.utils.js');
var React = require('react');

var linkedin = React.createClass({
  render: function() {
    return (
      <script type="in/Login"></script>
    );
  }
});

module.exports = linkedin;
    
    // Setup an event listener to make an API call once auth is complete
    function onLinkedInLoad() {
        IN.Event.on(IN, "auth", getProfileData);
    }

    // Handle the successful return from the API call
    function onSuccess(data) {
        console.log(data);
    }

    // Handle an error response from the API call
    function onError(error) {
        console.log(error);
    }

    // Use the API call wrapper to request the member's basic profile data
    function getProfileData() {
        IN.API.Raw("/people/~").result(onSuccess).error(onError);
    }
