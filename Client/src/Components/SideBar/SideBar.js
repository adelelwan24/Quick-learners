import UserCart from "./UserCart/UserCart";

const SideBar = () => {
    return (
    <div >
        <div >
            <h6 className='sidebar-title-me'>Users with similiar interest</h6>
        </div>
        
        <div className="SideBar-me-2">
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
    </div>
    
    );
}

export default SideBar;