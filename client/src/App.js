import React, { Component } from 'react';
import { BrowserRouter as Router, Route } from "react-router-dom";
import RateMyProfessor from './RateMyProfessor';

class App extends Component {
  render() {
    return (
        <Router>
            <div>
                <Route strict path="/rate-my-professor/" component={RateMyProfessor} />
            </div>
        </Router>
    );
  }
}

export default App;
