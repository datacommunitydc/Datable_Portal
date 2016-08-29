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

      var firstName = this.refs.firstName.value,
        lastName = this.refs.lastName.value,
        username = this.refs.username.value,
        email = this.refs.email.value,
        password = this.refs.password.value;

      AuthAction.register(firstName, lastName, username, email, password).then(() => {
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
            <label>First Name: </label>
            <input ref="firstName" placeholder="First name" className="form-control" defaultValue="" required/>
          </div>
          <div className="form-group"> 
            <label>Last Name: </label>
            <input ref="lastName" placeholder="Last name" className="form-control" defaultValue="" required/>
          </div>
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
