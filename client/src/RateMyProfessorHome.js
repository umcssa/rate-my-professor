import React from "react";

import {
    Card,
    Icon
} from 'antd';

const {Meta} = Card;

export default class RateMyProfessorHome extends React.Component {
    render() {
        return (
            <div style={{width:'100%',backgroundColor:'rgb(240,242,245)'}}>
                <Card
                    hoverable
                    style={{width: 240}}
                    cover={<div style={{background: '#ff4081', padding: 24, minHeight: 280}}>
                        <Icon style={{color: '#fff', padding: 60}} type="edit"/>
                    </div>}
                >
                    <Meta
                        title="发布新评价"
                        description="Rate My Professor"
                    />
                </Card>
            </div>
        )
    }
}
