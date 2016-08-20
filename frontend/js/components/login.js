var Linkedin = require('./linkedin');
var React = require('react');
var BrowserHistory = require('react-router').browserHistory;
var Auth = require('../services/auth');

var Login = React.createClass({
  getInitialState() {
    return {
        error: false
    }
  },

  handleSubmit(event) {
      event.preventDefault()

      const email = this.refs.email.value
      const pass = this.refs.pass.value

      Auth.login(email, pass, (loggedIn) => {
        if (!loggedIn)
          return this.setState({ error: true })

        BrowserHistory.push({
            pathname: '/'
        })
      })
  },

  render: function() {
    return (
      <div className="col-md-4">
        <form onSubmit={this.handleSubmit}>
          <div className="form-group"> 
            <label>Username: </label>
            <input ref="email" placeholder="Username" className="form-control" defaultValue="" />
          </div>
          <div className="form-group">
            <label>Password: </label>
            <input ref="pass" placeholder="password" className="form-control" />
          </div>
          <button className="btn btn-default" type="submit">Login</button>
        </form>
        <div className="marginT10">
            <Linkedin />
        </div>
      </div>
    );
  }
});

module.exports = Login;
