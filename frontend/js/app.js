var React = require('react');
var ReactDom = require('react-dom');
var ReactRouter = require('react-router');
var Router = ReactRouter.Router;
var Route = ReactRouter.Route; 
var browserHistory = ReactRouter.browserHistory; 
var Header = require('./components/header');
var Footer = require('./components/footer');
var Login = require('./components/login');
var Home = require('./components/home');
var WebAPIUtils = require('./utils/webapi.utils.js');
var Auth = require('./services/auth');

function requireAuth(nextState, replace) {
    if (!Auth.loggedIn()) {
        replace({ 
            pathname:'/login/',
            state: { nextPathname: '/' }
        })
    }
}

function isAuthenticated(nextState, replace) {
    if (Auth.loggedIn()) {
        replace({ 
            pathname:'/',
        })
    }
}

ReactDom.render(
  <div>
    <Header />
    <Router history={browserHistory}>
      <Route path='/' component={Home} onEnter={requireAuth}  />
      <Route path='/login' component={Login} onEnter={isAuthenticated} />
    </Router>
    <Footer />
  </div>,
  document.getElementById('react')
);
