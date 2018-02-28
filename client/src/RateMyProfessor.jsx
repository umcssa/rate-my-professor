import React from 'react';
import {
    BrowserRouter as Router,
    Route,
    Link,
} from 'react-router-dom';
import RateMyProfessorForm from './RateMyProfessorForm';
import RateMyProfessorSearch from './RateMyProfessorSearch';

const RateMyProfessor = ({match}) => (
    <div>
        <Route exact strict path={`${match.url}form/`} component={RateMyProfessorForm}/>
        <Route exact strict path={`${match.url}search/`} component={RateMyProfessorSearch}/>
        <Route
            exact strict
            path={match.url}
            render={() => <h3>Please select a topic.</h3>}
        />
    </div>
);

const Topic = ({ match }) => (
    <div>
        <h3>{match.params.topicId}</h3>
    </div>
);

export default RateMyProfessor;
