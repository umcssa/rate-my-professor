import React from "react";
import logo from "./CSSA_UM.jpeg";

import {
    Menu,
    Icon
} from 'antd';

const SubMenu = Menu.SubMenu;
const MenuItemGroup = Menu.ItemGroup;

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
    };

    handleClick = (e) => {
        console.log('click ', e);
        this.setState({
            current: e.key,
        });
    };

    render() {
        return (
            <Menu
                onClick={this.handleClick}
                selectedKeys={[this.state.current]}
                mode="horizontal"
                theme="dark"
                style={{position: 'fixed', top: 0, left: 0, width: '100%', zIndex: 999}}
            >
                <Menu.Item key="logo">
                    {/*<img src={logo} style={{height: 92}}/>*/}
                </Menu.Item>
                <Menu.Item key="mail">
                    <Icon type="mail"/>Navigation One
                </Menu.Item>
                <Menu.Item key="app">
                    <Icon type="appstore"/>Navigation Two
                </Menu.Item>
                <SubMenu title={<span><Icon type="setting"/>Navigation Three - Submenu</span>}>
                    <MenuItemGroup title="Item 1">
                        <Menu.Item key="setting:1">Option 1</Menu.Item>
                        <Menu.Item key="setting:2">Option 2</Menu.Item>
                    </MenuItemGroup>
                    <MenuItemGroup title="Item 2">
                        <Menu.Item key="setting:3">Option 3</Menu.Item>
                        <Menu.Item key="setting:4">Option 4</Menu.Item>
                    </MenuItemGroup>
                </SubMenu>
                <Menu.Item key="alipay">
                    <a href="https://ant.design" target="_blank" rel="noopener noreferrer">Navigation Four - Link</a>
                </Menu.Item>
            </Menu>
        )
    }
}
