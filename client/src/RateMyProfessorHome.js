import React from "react";

import {
    Card,
    Icon,
    Col,
    Row
} from 'antd';

const {Meta} = Card;

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
            <div style={Object.assign({width: '100%', backgroundColor: '#f0f2f5'},centerParentStyle)}>
                <Row gutter={20} stylt={Object.assign(centerChildStyle)}>
                    <Col span={10}>
                        <Card
                            hoverable
                            style={{width: 240, alignItems: 'center'}}
                            cover={<div
                                style={Object.assign({
                                    background: '#ff4081',
                                    padding: 24,
                                    minHeight: 280
                                }, centerParentStyle)}>
                                <Icon style={Object.assign({color: '#fff', fontSize: 100}, centerChildStyle)}
                                      type="edit"/>
                            </div>}
                        >
                            <Meta
                                title="发布新评价"
                                description="Rate My Professor"
                            />
                        </Card>
                    </Col>
                    <Col span={8}>
                        <Card
                            hoverable
                            style={{width: 240, alignItems: 'center'}}
                            cover={<div
                                style={Object.assign({
                                    background: '#00bdd5',
                                    padding: 24,
                                    minHeight: 280
                                }, centerParentStyle)}>
                                <Icon style={Object.assign({color: '#fff', fontSize: 100}, centerChildStyle)}
                                      type="search"/>
                            </div>}
                        >
                            <Meta
                                title="检索评价"
                                description="Search For Comments"
                            />
                        </Card>
                    </Col>
                </Row>


            </div>
        )
    }
}
