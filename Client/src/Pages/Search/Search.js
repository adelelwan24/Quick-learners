import Header from "../../Components/Header/Header";
import SideBar from "../../Components/SideBar/SideBar";
import {useLocation} from 'react-router-dom';
import QueryAnswer from "../../Components/Content/QueryAnswer/QueryAnswer";
const Search = () => {
    const location = useLocation();
    const query = location.state.query
    const res = location.state.res
    console.log(location.state)
    return ( 
        <div className="container-me">
            <div className="header">
                <Header/>
            </div>
            <div className="sidebar">
                <SideBar/>
            </div>
            <div className="content">
                <h6>{query}</h6>
                {res.map(ress => <QueryAnswer id={ress.video_id} start={ress.start}/>)}

            </div>
        </div>
        );
}
 
export default Search;

