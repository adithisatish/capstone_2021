import React from "react"
import Navbar from "./Navbar"

const Layout = (props) => {
    return (
        <React.Fragment>
            <Navbar page={props.page}></Navbar>
            <div>
                {props.children}
            </div>
        </React.Fragment>
    )
}

export default Layout