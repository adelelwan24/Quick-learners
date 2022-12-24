import { useEffect, useState } from "react";
import UseFetch from "../../Methods/UseFetch";
import UserCart from "./UserCart/UserCart";

const SideBar = () => {
    const [logged_in, setLogged_in] = useState(false)
    const [users, setUsers] = useState([])
    const {data , _ , __} = UseFetch('/api/user_rec')
    useEffect(() => {
        if(data == null){
            return
        }
        setLogged_in(data.logged_in)
        setUsers(data.users_data)
        console.log(logged_in)
    },[data]);    
    
    return (
    <div >
       
        <>
        <div >
        
            {logged_in ? ( (users.length == 0) ? <>  <span>No recommended users yet</span></> : <></>) : <div className="text-center">  <span  style={{'fontSize':"15px" , 'color':'gray'}}>You need to sign up to get Recommended users</span>  </div>}
        </div>
        <div className="SideBar-me-2">
            {logged_in ?<div className='sidebar-title-me'><h6 >Users with similiar interest</h6></div>:<></>}
            {users && users.map( (user)=> <UserCart name={user.name}  username={user.username}  key={user.username} />)}
            
        </div>
        </>
    </div>
    
    );
}

export default SideBar;