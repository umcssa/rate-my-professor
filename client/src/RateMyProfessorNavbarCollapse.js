import React from "react";
import {
    Navbar,
    Nav,
    NavItem,
    NavDropdown,
    MenuItem
} from 'react-bootstrap';
import logoM from "./images/logo-M.png";
import logoCSSA from "./images/logo-CSSA.png";


const hoverStyle = {
    backgroundColor: '#080808',
};


export default class RateMyProfessorNavbarCollapse extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            hover: [false, false, false],
        };
        this.handleMouseEnter = this.handleMouseEnter.bind(this);
        this.handleMouseLeave = this.handleMouseLeave.bind(this);
    }

    handleMouseEnter(id) {
        this.setState(prevState => {
            const newHover = prevState.hover.slice();
            newHover[id] = true;
            return {hover: newHover};
        });
    }

    handleMouseLeave(id) {
        this.setState(prevState => {
            const newHover = prevState.hover.slice();
            newHover[id] = false;
            return {hover: newHover};
        });
    }


    render() {
        return (
            <Navbar inverse collapseOnSelect
                    style={{
                        position: 'fixed',
                        width: '100%',
                        zIndex: 9999,
                        top: 0,
                        left: 0,
                        margin: 0,
                        borderRadius: 0,
                        borderWidth: 0,
                        backgroundColor: '#001529'
                    }}>
                <Navbar.Header>
                    <Navbar.Brand>
                        <a style={{paddingLeft: 20, paddingTop: 0}}><img src={logoM} style={{height: 50}}/></a>
                    </Navbar.Brand>
                    <Navbar.Toggle/>
                </Navbar.Header>
                <Navbar.Collapse>
                    <Nav>
                        <NavItem href="#">
                            CSSA APPs
                        </NavItem>
                    </Nav>
                    <Nav pullRight>
                        <NavDropdown title="Rate My Professor" id="basic-nav-dropdown-0"
                                     style={this.state.hover[0]? hoverStyle : {}}
                                     onMouseEnter={() => {
                                         this.handleMouseEnter(0);
                                     }}
                                     onMouseLeave={() => {
                                         this.handleMouseLeave(0);
                                     }}>
                            <MenuItem href="/rate-my-professor/form/">发布评价</MenuItem>
                            <MenuItem href="/rate-my-professor/search/">搜索评价</MenuItem>
                        </NavDropdown>
                        <NavDropdown eventKey={3} title="Freshman Handbook" id="basic-nav-dropdown-1"
                                     style={this.state.hover[1] ? hoverStyle : {}}
                                     onMouseEnter={() => {
                                         this.handleMouseEnter(1);
                                     }}
                                     onMouseLeave={() => {
                                         this.handleMouseLeave(1);
                                     }}>
                            <MenuItem href="/freshman-handbook/出国前准备/">出国前准备</MenuItem>
                            <MenuItem href="/freshman-handbook/入学指南/">入学指南</MenuItem>
                            <MenuItem href="/freshman-handbook/超市购物/">超市购物</MenuItem>
                            <MenuItem href="/freshman-handbook/休闲娱乐/">休闲娱乐</MenuItem>
                            <MenuItem href="/freshman-handbook/交通/">交通</MenuItem>
                            <MenuItem href="/freshman-handbook/社团介绍/">社团介绍</MenuItem>
                        </NavDropdown>
                        <NavDropdown title="Secondary Market" id="basic-nav-dropdown-2"
                                     style={this.state.hover[2]? hoverStyle : {}}
                                     onMouseEnter={() => {
                                         this.handleMouseEnter(2);
                                     }}
                                     onMouseLeave={() => {
                                         this.handleMouseLeave(2);
                                     }}>
                            <MenuItem href="/secondary-market/buy/">我要购买</MenuItem>
                            <MenuItem href="/secondary-market/sell/">我要出售</MenuItem>
                        </NavDropdown>
                        <NavItem href="http://www.um-cssa.org/" target="_blank">
                            <img src={logoCSSA} style={{height: 50, padding: 0}}/>
                        </NavItem>
                    </Nav>
                </Navbar.Collapse>
            </Navbar>
        )
    }
}
