import useFetch from "../../Methods/UseFetch";
import UserCart from "./UserCart/UserCart";

const SideBar = () => {
    const logged_in = true
    // const {logged_in,users} = useFetch('/recusers')
    return (
    <div >
        { logged_in &&
        <>
        <div >
            <h6 className='sidebar-title-me'>Users with similiar interest</h6>
        </div>
        
        <div className="SideBar-me-2">
            {/* {logged_in && users.map(user=> <UserCart name={user.name}  username={user.username}   />)} */}
            <UserCart/>
            <UserCart/>
            <UserCart/>
            <UserCart/>
            <UserCart/>
            <UserCart/>
            <UserCart/>
            <UserCart/>
            <UserCart/>
            <UserCart/>
            <UserCart/>
            <UserCart/>
            <UserCart/>
            <UserCart/>
            <UserCart/>
        </div>
        </>}
    </div>
    
    );
}

export default SideBar;