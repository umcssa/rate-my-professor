import React from 'react';
import {Menu, Icon} from 'antd';
import logoM from "./images/logo-M.png";
import logoCSSA from "./images/logo-CSSA.png";

const SubMenu = Menu.SubMenu;
const MenuItemGroup = Menu.ItemGroup;

const activeStyle = {
    backgroundColor: '#1890ff',
    color: '#ffffff'
};

const centerParentStyle = {
    display: 'table'
};

const centerChildStyle = {
    display: 'table-cell',
    verticalAlign: 'middle',
    textAlign: 'center',
};

export default class RateMyProfessorNavbar extends React.Component {
    state = {
        current: 'mail',
        collapsed: true,
    }
    toggleCollapsed = () => {
        this.setState({
            collapsed: !this.state.collapsed,
        });
    }


    render() {
        return (
            <Menu
                theme="dark"
                onClick={this.handleClick}
                selectedKeys={[this.state.current]}
                mode="horizontal"
                style={{position:'fixed',width:'100%', top:0, left:0}}
            >
                <Menu.Item key="logoM" style={{height: 46, width: 70, marginLeft: 20}}>
                    <a href="/">
                        <img src={logoM}
                             style={{
                                 height: 40,
                                 position: 'absolute',
                                 margin: 'auto',
                                 top: 0,
                                 left: 0,
                                 right: 0,
                                 bottom: 0
                             }}/>
                    </a>
                </Menu.Item>

                <Menu.Item key="apps">
                    <a href="/" style={{color:'#ffffff', fontSize:20}}>CSSA APPs</a>
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
                             }}/>
                    </a>
                </Menu.Item>
                <SubMenu title={<span onClick={() => {
                    window.location.href = "/secondary-market/";
                }}><Icon type="shopping-cart" />Secondary Market</span>}
                         style={Object.assign({float: 'right'}, window.location.href.includes('secondary-market') && activeStyle)}>
                    <Menu.Item key="1">我要购买</Menu.Item>
                    <Menu.Item key="2">我要出售</Menu.Item>
                </SubMenu>
                <SubMenu title={<span onClick={() => {
                    window.location.href = "/freshman-handbook/";
                }}><Icon type="book"/>Freshman Handbook</span>}
                         style={Object.assign({float: 'right'}, window.location.href.includes('freshman-handbook') && activeStyle)}>
                    <Menu.Item key="1">出国前准备</Menu.Item>
                    <Menu.Item key="2">入学指南</Menu.Item>
                    <Menu.Item key="3">超市购物</Menu.Item>
                    <Menu.Item key="4">休闲娱乐</Menu.Item>
                    <Menu.Item key="5">交通</Menu.Item>
                    <Menu.Item key="6">社团介绍</Menu.Item>
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