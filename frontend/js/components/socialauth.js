var Linkedin = require('./linkedin');
var React = require('react');

var SocialAuth = React.createClass({
  render: function() {
    return (
      <div>
        <Linkedin />
      </div>
    );
  }
});

module.exports = SocialAuth;
