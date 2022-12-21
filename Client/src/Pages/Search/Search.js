import Header from "../../Components/Header/Header";
import SideBar from "../../Components/SideBar/SideBar";
import {useLocation} from 'react-router-dom';
import QueryAnswer from "../../Components/Content/QueryAnswer/QueryAnswer";
const Search = () => {
    const location = useLocation();
    const query = location.state.query
    const res = location.state.resJson
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
                <div className="post-me">
                    <h5 >Query: {query}</h5>
                </div>
                
                { res && res.map(ress => <QueryAnswer id={ress.video_id} start={ress.start} text={ress.text}/>)}

            </div>
        </div>
        );
}
 
export default Search;

