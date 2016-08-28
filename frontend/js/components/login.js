var React = require('react');
var BrowserHistory = require('react-router').browserHistory;
var AuthAction = require('../actions/auth');
var AuthStore = require('../stores/auth');
var proxy = require('../constants/webapi').proxy;

var Login = React.createClass({
  contextTypes: {
      router: React.PropTypes.object.isRequired
  },

  handleSubmit: function(e) {
      e.preventDefault()

      var username = this.refs.username.value
      var password = this.refs.password.value

      AuthAction.logIn(username, password).then(() => {
        this.context.router.replace('/');
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
            <label>Password: </label>
            <input type="password" ref="password" placeholder="password" className="form-control" required/>
          </div>
          <button className="btn btn-default" type="submit">Login</button>
        </form>
        <div className="marginT10">
          <a href="/register">New User? Create Account</a>
        </div>
        <div className="marginT10">
          <a href={ proxy + '/accounts/google/login/' } className="icon linkedin"><i className="fa fa-linkedin"></i></a>
          <a className="icon github"><i className="fa fa-github"></i></a>
          <a href={ proxy + '/accounts/twitter/login/' } className="icon linkedin"><i className="fa fa-twitter"></i></a>
        </div>
      </div>
    );
  }
});

module.exports = Login;
