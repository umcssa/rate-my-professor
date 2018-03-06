import React from 'react';
import {
    BrowserRouter as Router,
    Route,
    Link,
} from 'react-router-dom';
import RateMyProfessorNavbar from './RateMyProfessorNavbar';
import RateMyProfessorHome from './RateMyProfessorHome';
import RateMyProfessorForm from './RateMyProfessorForm';
import RateMyProfessorSearch from './RateMyProfessorSearch';

const RateMyProfessor = ({match}) => (
    <div>
        <RateMyProfessorNavbar />
        <Route exact strict path={`${match.url}form/`} component={RateMyProfessorForm}/>
        <Route exact strict path={`${match.url}search/`} component={RateMyProfessorSearch}/>
        <Route exact strict path={match.url} component={RateMyProfessorHome} />
    </div>
);

const Topic = ({match}) => (
    <div>
        <h3>{match.params.topicId}</h3>
    </div>
);

export default RateMyProfessor;
