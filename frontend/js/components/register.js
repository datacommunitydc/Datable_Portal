var Linkedin = require('./linkedin');
var React = require('react');
var AuthAction = require('../actions/auth');
var AuthStore = require('../stores/auth');

var Register = React.createClass({
  contextTypes: {
      router: React.PropTypes.object.isRequired
  },

  handleSubmit: function(e) {
      e.preventDefault()

      var username = this.refs.username.value
      var email = this.refs.email.value
      var password = this.refs.password.value

      AuthAction.register(username, email, password).then(() => {
        AuthAction.logIn(username, password).then(() => {
            this.context.router.replace('/');
        });
      });
  },

  render: function() {
    return (
      <div className="login-container">
        <form onSubmit={this.handleSubmit}>
          <div className="form-group"> 
            <label>Username: </label>
            <input ref="username" placeholder="Username" className="form-control" defaultValue="" required/>
          </div>
          <div className="form-group"> 
            <label>Email: </label>
            <input type="email" ref="email" placeholder="Email" className="form-control" defaultValue="" required/>
          </div>
          <div className="form-group">
            <label>Password: </label>
            <input type="password" ref="password" placeholder="password" className="form-control" required/>
          </div>
          <button className="btn btn-default" type="submit">Sign Up</button>
        </form>
      </div>
    );
  }
});

module.exports = Register;
