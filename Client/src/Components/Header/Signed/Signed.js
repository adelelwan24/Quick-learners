import { useNavigate } from "react-router-dom";
import UseFetch from "../../../Methods/UseFetch";
import { useState,useEffect ,useContext} from "react";
import { LoggedinContext } from "../Header";

const Signed = () => {
    const {setLoggedin , loggedin} = useContext(LoggedinContext);
    const navigate = useNavigate();
    //ERROR handlin
    //Data 
    const [data,setData] = useState(null)
    

    const handlesignout = () =>{
        const abortContr = new AbortController();  
        fetch("/api/logout" ,{signal : abortContr.signal})
        .then(list => {
            if (!list.ok){
                throw Error("couldn't find data at this resource");
            }
            return list.json()
        })
        .then(jsonList => {
            setData(jsonList);
            console.log(jsonList)
        })
        .then(()=>{
            
            setLoggedin(false)
        })
        navigate('/signin');
        
    }

    return ( 
    <div>
        <button onClick={handlesignout} className="btn btn-outline-secondary" type="button">Sign Out</button>
    </div>
    );
}

export default Signed;