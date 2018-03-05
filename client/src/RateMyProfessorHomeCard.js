import React from "react";

import {
    Card,
    Icon,
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

export default class RateMyProfessorHomeCard extends React.Component {
    render() {
        return (

            <Card
                hoverable
                style={{width: 280, margin: 'auto'}}
                cover={<div
                    style={Object.assign({
                        background: this.props.backgroundColor,
                        minHeight: 280,
                        width: '100%'
                    }, centerParentStyle)}>
                    <Icon style={Object.assign({color: '#fff', fontSize: 100}, centerChildStyle)}
                          type={this.props.iconType}/>
                </div>}
            >
                <Meta
                    title={this.props.title}
                    description={this.props.description}
                />
            </Card>
        )
    }
}
