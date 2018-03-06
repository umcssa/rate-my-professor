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

export default class RateMyProfessorVerificationFail extends React.Component {
    render() {
        return (
            <div style={Object.assign({
                minHeight: window.innerHeight,
                width: '100%',
                backgroundColor: '#f0f2f5',
                padding: 40
            }, centerParentStyle)}>
                <div style={centerChildStyle}>
                    <Alert style={{maxWidth:1000, margin:'auto'}}
                        message="验证失败！"
                           description={<span>请使用正确的验证链接。如有疑问请咨询<a href="mailto:umcssapublicity@gmail.com">umcssapublicity@gmail.com</a>。</span>}
                        type="error"
                        showIcon
                    />
                </div>
            </div>
        )
    }
}
