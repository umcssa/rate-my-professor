import React from "react";
import {Link} from "react-router-dom";
import RateMyProfessorCard from './RateMyProfessorHomeCard';

import {
    Card,
    Icon,
    Col,
    Row
} from 'antd';

const centerParentStyle = {
    display: 'table'
};

const centerChildStyle = {
    display: 'table-cell',
    verticalAlign: 'middle',
    textAlign: 'center',
};

export default class RateMyProfessorHome extends React.Component {
    render() {
        return (
            <div style={Object.assign({
                minHeight: window.innerHeight,
                width: '100%',
                backgroundColor: '#f0f2f5',
                padding: 40
            }, centerParentStyle)}>

                <Row style={centerChildStyle}>
                    <Col sm={24} md={12} style={{paddingTop: 100, paddingBottom: 100}}>
                        <Link to={`${this.props.match.url}form/`}>
                            <RateMyProfessorCard backgroundColor="#ff4081" iconType="edit" title="发布评价"
                                                 description="I want to Rate"/>
                        </Link>
                    </Col>

                    <Col sm={24} md={12} style={{paddingTop: 100, paddingBottom: 100}}>
                        <Link to={`${this.props.match.url}search/`}>
                            <RateMyProfessorCard backgroundColor="#00bdd5" iconType="search" title="搜索评价"
                                                 description="I want to Search"/>
                        </Link>
                    </Col>
                </Row>
            </div>
        )
    }
}
