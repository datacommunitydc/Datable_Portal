var url = window.location.origin;
var proxy = 'datable_backend_app';
var linkedinProxy = 'linkedin';
var meetupProxy = 'meetup';
var twitterProxy = 'twitter';
var githubProxy = 'github';

module.exports = {
  BaseUrl: `${url}/${proxy}`,
  LinkedinUrl: `${url}/${linkedinProxy}`,
  MeetupUrl: `${url}/${meetupProxy}`,
  TwitterUrl: `${url}/${twitterProxy}`,
  GithubUrl: `${url}/${githubProxy}`  
};
