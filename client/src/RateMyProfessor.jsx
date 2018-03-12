import React from 'react';
import { Route } from 'react-router-dom';
import RateMyProfessorNavbar from './RateMyProfessorNavbar';
import RateMyProfessorNavbarCollapse from './RateMyProfessorNavbarCollapse';
import RateMyProfessorHome from './RateMyProfessorHome';
import RateMyProfessorForm from './RateMyProfessorForm';
import RateMyProfessorSearch from './RateMyProfessorSearch';
import RateMyProfessorVerificationSuccess from './RateMyProfessorVerificationSuccess';
import RateMyProfessorVerificationFail from './RateMyProfessorVerificationFail';

const RateMyProfessor = ({match}) => (
    <div>
        {window.innerWidth < 992 ? <RateMyProfessorNavbarCollapse/> : <RateMyProfessorNavbar/>}
        <Route exact strict path={`${match.url}form/`} component={RateMyProfessorForm}/>
        <Route exact strict path={`${match.url}search/`} component={RateMyProfessorSearch}/>
        <Route exact strict path={`${match.url}verification-success/`} component={RateMyProfessorVerificationSuccess}/>
        <Route exact strict path={`${match.url}verification-fail/`} component={RateMyProfessorVerificationFail}/>
        <Route exact strict path={match.url} component={RateMyProfessorHome} />
    </div>
);

export default RateMyProfessor;
