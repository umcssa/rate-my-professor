import React from "react";

import {Alert} from 'antd';


const centerParentStyle = {
    display: 'table'
};

const centerChildStyle = {
    display: 'table-cell',
    verticalAlign: 'middle',
    textAlign: 'center',
};

export default class RateMyProfessorVerificationSuccess extends React.Component {
    render() {
        return (
            <div style={Object.assign({
                minHeight: window.innerHeight,
                width: '100%',
                backgroundColor: '#f0f2f5',
                padding: 40
            }, centerParentStyle)}>
                <div style={centerChildStyle}>
                    <Alert
                        message="Success Tips"
                        description="Detailed description and advices about successful copywriting."
                        type="success"
                        showIcon
                    />
                </div>
            </div>
        )
    }
}
