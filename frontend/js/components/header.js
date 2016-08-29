var React = require('react');
var AuthStore = require('../stores/auth');
var AuthAction = require('../actions/auth');

function getStates() {
  AuthStore.getProfile().then((res) => { console.log(res) });
  return {
      loggedIn: AuthStore.loggedIn()
  };
}

var header = React.createClass({
  getInitialState() {
    return getStates(); 
  },

  contextTypes: {
    // router: React.PropTypes.object.isRequired
  },

  componentDidMount: function(callback) {
    AuthStore.addChangeListener(this._onChange);
  },

  _onChange: function() {
     this.setState(getStates());
  },

  logOut: function () {
    AuthAction.logOut();
  },

  render: function() {
    return (
      <header> 
        <div className='header-title'>Datable</div>
        <div className="user-details">
          { this.state.loggedIn ? (
              <a href="#" onClick={this.logOut}>Logout</a>
            ) : (
              <a href="/login">Sign In</a>
            ) }
        </div>
      </header>
    );
  }
});

module.exports = header;