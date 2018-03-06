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
                    <Alert style={{maxWidth:1000, margin:'auto'}}
                        message="验证成功！"
                           description={<span>感谢您的参与！您的评价已发布，可前往<a href="/rate-my-professor/search/">搜索界面</a>查看。</span>}
                        type="success"
                        showIcon
                    />
                </div>
            </div>
        )
    }
}
