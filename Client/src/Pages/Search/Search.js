import Content from "../../Components/Content/Content";
import Header from "../../Components/Header/Header";
import SideBar from "../../Components/SideBar/SideBar";
import {useLocation} from 'react-router-dom';
const Search = () => {
    const location = useLocation();
    console.log(location.state  )
    return ( 
        <div className="container-me">
            <div className="header">
                <Header/>
            </div>
            <div className="sidebar">
                <SideBar/>
            </div>
            <div className="content">
                <p>{location.state.query}</p>
                <Content/>    
            </div>
        </div>
        );
}
 
export default Search;

