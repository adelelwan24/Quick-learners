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
                <p>because the website is still in development phase you can only search in these two playlists:</p>
                <div style={{"marginBottom":"35px"}}>
                    
                        <li>
                            <a href="https://www.youtube.com/playlist?list=PLUl4u3cNGP619EG1wp0kT-7rDE_Az5TNd">MIT 6.0002 Intro to Computational Thinking and Data Science</a>
                        </li>
                        <li>
                            <a href="https://www.youtube.com/playlist?list=PLUl4u3cNGP60uVBMaoNERc6knT_MgPKS0">MIT 18.650 Statistics for Applications, Fall 2016</a>
                        </li>
                    
                </div>
                <div className="post-me">
                    <h5 >Query: {query}</h5>
                </div>
                
                { res && res.map(ress => <QueryAnswer id={ress.video_id} start={ress.start} text={ress.text}/>)}

            </div>
        </div>
        );
}
 
export default Search;

