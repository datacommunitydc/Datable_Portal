var React = require('react');
var ReactDom = require('react-dom');
var ReactRouter = require('react-router');
var Router = ReactRouter.Router;
var Route = ReactRouter.Route; 
var browserHistory = ReactRouter.browserHistory; 
var Header = require('./components/header');
var Footer = require('./components/footer');
var SocialAuth = require('./components/socialauth');
var LinkedinAuth = require('./components/linkedin_auth');
var Home = require('./components/home');
var WebAPIUtils = require('./utils/webapi.utils.js');

ReactDom.render(
  <div>
    <Header />
    <Router history={browserHistory}>
      <Route path='/' component={Home} />
      <Route path='/social' component={SocialAuth} />
      <Route path='/linkedin-auth' component={LinkedinAuth} onEnter={getLinkedinAccessToken} />
      <Route path='/linkedin-auth1' component={Footer} />
    </Router>
    <Footer />
  </div>,
  document.getElementById('react')
);

function getLinkedinAccessToken() {
  var code = getAccessToken('code');
    // if(authToken && window.opener && window.opener.setAccessToken) {
    //     window.opener.setAccessToken(authToken);
    // }
    //window.close();
    if(code) {
        console.log(code)
        WebAPIUtils.getLinkedinAccessToken(code)
    }
}
function getAccessToken(indentifier) {
    var hash = window.location.href;
    if(hash) {
        var startIndex = hash.indexOf(indentifier+'='),
            lastIndex = hash.indexOf('&', startIndex);

        return startIndex > 0 && lastIndex > 0 ? hash.slice(startIndex + (indentifier + '=').length, lastIndex) : '';
    } else {
        return '';
    }
}