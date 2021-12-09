import React from "react"
import { connect } from "react-redux"
import { 
    Menu, MenuItem, Drawer,
    Divider, List, ListItem,
    ListItemText
} from "@material-ui/core"
import { logout } from "../../actions/auth"

const Navbar = (props) => {
    const [anchorEl, setAnchorEl] = React.useState(null);
    const [isDrawerOpen, setDrawerOpen] = React.useState(false);

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
            <div className='mr-2 lg:hidden' onClick={() => setDrawerOpen(true)}>
                <svg xmlns="http://www.w3.org/2000/svg" class="icon icon-tabler icon-tabler-menu-2" width="24" height="24" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" fill="none" stroke-linecap="round" stroke-linejoin="round">
                    <path stroke="none" d="M0 0h24v24H0z" fill="none"></path>
                    <line x1="4" y1="6" x2="20" y2="6"></line>
                    <line x1="4" y1="12" x2="20" y2="12"></line>
                    <line x1="4" y1="18" x2="20" y2="18"></line>
                </svg>
            </div>
            <p>Capstone</p>
            <div className="flex flex-grow ml-6 ph:hidden">
                {leftElement}
            </div>
            <div className="flex ph:hidden">
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

            <Drawer anchor='left' open={ isDrawerOpen } onClose={ () => setDrawerOpen(false) }>
                <div className='w-48' role="presentation" onClick={ () => setDrawerOpen(false) } >
                    <p className='font-green-800 text-4xl font-bold ml-2 mt-2 mb-2'>Capstone</p>
                    <Divider />
                    <List>
                        {props.user? (
                            <React.Fragment>
                                <ListItem button onClick={() => window.location.href = `/deconstructor`}>
                                    <ListItemText primary='Deconstructor' />
                                </ListItem>
                                <ListItem button>
                                    <ListItemText primary='Logout' onClick={() => logout()}/>
                                </ListItem>
                            </React.Fragment>
                        ): (
                            <React.Fragment>
                                <ListItem button onClick={() => window.location.href = `/login`}>
                                    <ListItemText primary='Login/Signup' />
                                </ListItem>
                            </React.Fragment>
                        )}
                    </List>
                </div>
            </Drawer>
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