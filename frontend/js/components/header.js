var React = require('react');
var AuthStore = require('../stores/auth');
var AuthAction = require('../actions/auth');
var BrowserHistory = require('react-router').browserHistory;

var header = React.createClass({
  getInitialState() {
    return {
      loggedIn: AuthStore.loggedIn(),
      profile: {first_name: '', last_name: ''}
    }; 
  },

  componentDidMount: function(callback) {
    AuthStore.addChangeListener(this._onChange);

    //profile api call
    this._getProfile()
  },

  _getProfile: function() {
    AuthStore.getProfile().then((res, err) => { 
      if(res) {
        this.setState({
          loggedIn: AuthStore.loggedIn(),
          profile: res.body
        })
      }
    });
  },

  _onChange: function() {
     if(AuthStore.loggedIn()) {
       this._getProfile()
     } else {
      this.setState({
        loggedIn: AuthStore.loggedIn(),
        profile: {first_name: '', last_name: ''}
      })
     }
  },

  logOut: function () {
    AuthAction.logOut().then((res, err) => {
        BrowserHistory.push('/login')
      });
  },

  render: function() {
    return (
      <header> 
        <div className='header-title'>Datable</div>
        <div className="user-details">
          { this.state.loggedIn ? (
              <div>
                <div className="username">
                  Welcome {this.state.profile.first_name} {this.state.profile.last_name}
                </div>
                <a href="#" onClick={this.logOut}>Logout</a>
              </div>
            ) : (
              <a href="/login">Sign In</a>
            ) }
        </div>
      </header>
    );
  }
});

module.exports = header;