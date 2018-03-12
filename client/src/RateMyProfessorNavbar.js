import React from 'react';
import {Menu, Icon} from 'antd';
import logoCSSAAPPs from "./images/cssa_apps_white.png";
import logoCSSA from "./images/logo-CSSA.png";
import './RateMyProfessorNavbar.css';

const SubMenu = Menu.SubMenu;

const activeStyle = {
    backgroundColor: '#1890ff',
    color: '#ffffff'
};


export default class RateMyProfessorNavbar extends React.Component {
    state = {
        current: 'mail',
        collapsed: true,
    };

    toggleCollapsed = () => {
        this.setState({
            collapsed: !this.state.collapsed,
        });
    };

    render() {
        return (
            <Menu
                theme="dark"
                onClick={this.handleClick}
                selectedKeys={[this.state.current]}
                mode="horizontal"
                style={{position: 'fixed', width: '100%', top: 0, left: 0, zIndex: 9999}}
            >
                <Menu.Item key="logoCSSAAPPs" style={{height: 46, width: 70, marginLeft: 20}}>
                    <a href="/">
                        <img src={logoCSSAAPPs}
                             style={{
                                 height: 36,
                                 position: 'absolute',
                                 margin: 'auto',
                                 top: 0,
                                 left: 0,
                                 right: 0,
                                 bottom: 0
                             }}
                             alt="CSSA APPs"/>
                    </a>
                </Menu.Item>

                <Menu.Item key="apps">
                    <a href="/" style={{color: '#ffffff', fontSize: 20}}>CSSA APPs</a>
                </Menu.Item>

                <Menu.Item key="logoCSSA" style={{float: 'right', height: 46, width: 70}}>
                    <a href="http://www.um-cssa.org/" target="__blank">
                        <img src={logoCSSA}
                             style={{
                                 height: 40,
                                 position: 'absolute',
                                 margin: 'auto',
                                 top: 0,
                                 left: 0,
                                 right: 0,
                                 bottom: 0
                             }}
                             alt="UM-CSSA"/>
                    </a>
                </Menu.Item>
                <SubMenu title={<span onClick={() => {
                    window.location.href = "/secondary-market/";
                }}><Icon type="shopping-cart"/>Secondary Market</span>}
                         style={Object.assign({float: 'right'}, window.location.href.includes('secondary-market') && activeStyle)}>
                    <Menu.Item key="1"><a href="/secondary-market/buy/">我要购买</a></Menu.Item>
                    <Menu.Item key="2"><a href="/secondary-market/sell/">我要出售</a></Menu.Item>
                </SubMenu>
                <SubMenu title={<span onClick={() => {
                    window.location.href = "/freshman-handbook/";
                }}><Icon type="book"/>Freshman Handbook</span>}
                         style={Object.assign({float: 'right'}, window.location.href.includes('freshman-handbook') && activeStyle)}>
                    <Menu.Item key="1"><a href="/freshman-handbook/出国前准备/">出国前准备</a></Menu.Item>
                    <Menu.Item key="2"><a href="/freshman-handbook/入学指南/">入学指南</a></Menu.Item>
                    <Menu.Item key="3"><a href="/freshman-handbook/超市购物/">超市购物</a></Menu.Item>
                    <Menu.Item key="4"><a href="/freshman-handbook/休闲娱乐/">休闲娱乐</a></Menu.Item>
                    <Menu.Item key="5"><a href="/freshman-handbook/交通/">交通</a></Menu.Item>
                    <Menu.Item key="6"><a href="/freshman-handbook/社团介绍/">社团介绍</a></Menu.Item>
                </SubMenu>
                <SubMenu title={<span onClick={() => {
                    window.location.href = "/rate-my-professor/";
                }}><Icon type="like-o"/>Rate My Professor</span>}
                         style={Object.assign({float: 'right'}, window.location.href.includes('rate-my-professor') && activeStyle)}>
                    <Menu.Item key="1"><a href="/rate-my-professor/form/">发布评价</a></Menu.Item>
                    <Menu.Item key="2"><a href="/rate-my-professor/search/">搜索评价</a></Menu.Item>
                </SubMenu>
            </Menu>
        );
    }
}