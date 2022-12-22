import SearchBar from "./SearchBar/SearchBar";
import NotSigned from "./NotSigned/NotSigned";
import SiteName from "./SiteName/SiteName";
import UseFetch from "../../Methods/UseFetch";
import Signed from "./Signed/Signed";
import { useEffect, useState,createContext  } from "react";

export const LoggedinContext = createContext(false);

const Header = () => {
    
    
    const [loggedin , setLoggedin] = useState(false)
    let {data, error, isPending} = UseFetch('/api/logged_in')
    // console.log(error)
    
    console.log(data)
    useEffect(() => {
        if(data == null){
            return
        }
        setLoggedin(data.logged_in)
    },[data]);


    return ( 
        <div className="header-me">
            <div className="header-me-1">
                <SiteName/>
            </div>
            <div className="header-me-2">
                <SearchBar/>
            </div>
            <div className="header-me-3">
                <LoggedinContext.Provider value={{setLoggedin , loggedin}}>
                {loggedin ? <Signed/>:  <NotSigned/> }
                </LoggedinContext.Provider>
            </div>
            
        </div>
    );
}

export default Header;