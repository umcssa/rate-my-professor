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
                        zIndex: 999,
                        top: 0,
                        left: 0,
                        margin: 0,
                        borderRadius: 0,
                        borderWidth: 0,
                        backgroundColor: '#0c142d'
                    }}>
                <Navbar.Header>
                    <Navbar.Brand>
                        <a style={{paddingLeft: 50, paddingTop: 0}}><img src={logoM} style={{height: 50}}/></a>
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
                        <NavDropdown title="Rate My Professor" id="basic-nav-dropdown-1"
                                     style={this.state.hover[0]? hoverStyle : {}}
                                     onMouseEnter={() => {
                                         this.handleMouseEnter(0);
                                     }}
                                     onMouseLeave={() => {
                                         this.handleMouseLeave(0);
                                     }}>
                            <MenuItem>发布评价</MenuItem>
                            <MenuItem>搜索评价</MenuItem>
                        </NavDropdown>
                        <NavDropdown eventKey={3} title="Freshman Handbook" id="basic-nav-dropdown-2"
                                     style={this.state.hover[1] ? hoverStyle : {}}
                                     onMouseEnter={() => {
                                         this.handleMouseEnter(1);
                                     }}
                                     onMouseLeave={() => {
                                         this.handleMouseLeave(1);
                                     }}>
                            <MenuItem>出国前准备</MenuItem>
                            <MenuItem>入学指南</MenuItem>
                            <MenuItem>超市购物</MenuItem>
                            <MenuItem>休闲娱乐</MenuItem>
                            <MenuItem>交通</MenuItem>
                            <MenuItem>社团介绍</MenuItem>
                        </NavDropdown>
                        <NavItem href="#"
                                 style={this.state.hover[2] ? hoverStyle : {}}
                                 onMouseEnter={() => {
                                     this.handleMouseEnter(2);
                                 }}
                                 onMouseLeave={() => {
                                     this.handleMouseLeave(2);
                                 }}>
                            Secondary Market
                        </NavItem>
                        <NavItem href="http://www.um-cssa.org/" target="_blank">
                            <img src={logoCSSA} style={{height: 50, padding: 0}}/>
                        </NavItem>
                    </Nav>
                </Navbar.Collapse>
            </Navbar>
        )
    }
}
