var React = require('react');
var AuthStore = require('../stores/auth');

var home = React.createClass({
  getInitialState() {
    return {
      sections: undefined
    };
  },

  componentDidMount: function(callback) {
    AuthStore.getQuestions().then((res, err) => {
      if(res) {
        let sections = res.body.sections;
        this.setState({
          sections: sections
        });
      }
    });
  },

  render: function() {
    return (
      <div>
        {(() => {
          if (this.state.sections) {
            for (let index = 0; index < this.state.sections.length; index++) {
              var section = this.state.sections[index];
              return <div>
                <h3> { section.title } </h3>
                <div>
                  {
                    section.questions.map(function(question) {
                      return <div key={ 'question_' + question.id}>
                        <div> { question.question } </div>
                        <div>
                          {(() => {
                            switch (question.type) {
                              case "text": return <input type="text" />;
                              case "radio":
                                var options = [];
                                for (var index = 0; index < question.options.length; index++) {
                                  var option = question.options[index];
                                  options.push(<div><input type="radio" value={option.value} /> {option.text}</div>)
                                }
                                return options;
                                break;
                              case "checkbox":
                                var options = [];
                                for (var index = 0; index < question.options.length; index++) {
                                  var option = question.options[index];
                                  options.push(<div><input type="checkbox" value={option.value} /> {option.text}</div>)
                                }
                                return options;
                                break;
                            }
                          })()}
                        </div>
                      </div>
                    })
                  }
                </div>
              </div>
            }
          } else {
            return "No Questions";
          }
        })()}
      </div>
    );
  }
});

module.exports = home;
