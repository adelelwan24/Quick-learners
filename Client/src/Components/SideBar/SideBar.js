import { useEffect, useState } from "react";
import useFetch from "../../Methods/UseFetch";
import UserCart from "./UserCart/UserCart";

const SideBar = () => {
    const [logged_in, setLogged_in] = useState(false)
    const [users, setUsers] = useState([])
    const {data , error , isPending} = useFetch('/api/user_rec')
    useEffect(() => {
        if(data == null){
            return
        }
        setLogged_in(data.logged_in)
        setUsers(data.users)
    },[data]);    
    
    return (
    <div >
        { logged_in &&
        <>
        <div >
            {users && <h6 className='sidebar-title-me'>Users with similiar interest</h6>}   
        </div>
        <div className="SideBar-me-2">

            {users && users.map( (user)=> <UserCart name={user.name}  username={user.username}   />)}
            
        </div>
        </>}
    </div>
    
    );
}

export default SideBar;