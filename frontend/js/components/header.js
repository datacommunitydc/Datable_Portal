var React = require('react');
var Auth = require('../services/auth');
var Link = require('react-router').Link;

var header = React.createClass({
  getInitialState() {
    return {
      loggedIn: Auth.loggedIn()
    }
  },

  updateAuth(loggedIn) {
    this.setState({
      loggedIn
    })
  },

  componentWillMount() {
    Auth.onChange = this.updateAuth
    Auth.login()
  },

  render: function() {
    return (
      <header> 
        <div className='header-title'>Datable</div>
        <div className="user-details">
          { this.state.loggedIn ? (
              <a href="#" onClick={this.logout}>Logout</a>
            ) : (
              <a href="/login">Sign In</a>
            ) }
        </div>
      </header>
    );
  },

  logout: function () {
    Auth.logout(function() {

    });
  }
});

module.exports = header;