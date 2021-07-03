import React from "react"
import { connect } from "react-redux"
import { Menu, MenuItem } from "@material-ui/core"
import { logout } from "../../actions/auth"

const Navbar = (props) => {
    const [anchorEl, setAnchorEl] = React.useState(null);

    const handleClick = (event) => {
        setAnchorEl(event.currentTarget);
    };

    let rightElement = (
        <div className="cursor-pointer" onClick={handleClick}>
            <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-user" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                <circle cx="12" cy="7" r="4"></circle>
                <path d="M6 21v-2a4 4 0 0 1 4 -4h4a4 4 0 0 1 4 4v2"></path>
            </svg>
        </div>
    )

    if(!props.isLoggedIn){
        if(props.page=="landing"){
            rightElement = (
                <div className="cursor-pointer" onClick={() => window.location.href='/login'}>
                    Login
                </div>
            )
        }
        else{
            rightElement = null
        }
    }

    let leftElement = null

    if(props.page==="landing"){
        if(props.isLoggedIn){
            leftElement = (
                <div className="cursor-pointer" onClick={() => window.location.href='/deconstructor'}>
                    Deconstructor
                </div>
            )
        }
    } else{
        leftElement = (
            <div className="cursor-pointer" onClick={() => window.location.href='/'}>
                About Us
            </div>
        )
    }

    console.log(props.isLoggedIn)

    return (
        <div className="w-full bg-green-400 p-3 shadow-xl flex">
            <p>Capstone</p>
            <div className="flex flex-grow ml-6">
                {leftElement}
            </div>
            <div className="flex">
                {rightElement}
            </div>
            {
                props.isLoggedIn? (
                    <Menu
                        anchorEl={anchorEl}
                        keepMounted
                        open={Boolean(anchorEl)}
                        onClose={() => setAnchorEl(null)}
                        className="mt-4"
                    >
                        <MenuItem>{props.user.name}</MenuItem>
                        <MenuItem onClick={() => logout()}>Logout</MenuItem>
                    </Menu>
                ): null
            }
        </div>
    )
}

const mapStateToProps = (state) => {
    return {
        isLoggedIn: state.auth.loggedIn,
        user: state.auth.user
    }
}

export default connect(mapStateToProps)(Navbar);