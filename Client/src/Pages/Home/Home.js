import Content from "../../Components/Content/Content";
import Header from "../../Components/Header/Header";
import SideBar from "../../Components/SideBar/SideBar";
const Home = () => {
    return ( 
    <div className="container-me">
        <div className="header">
            <Header/>
        </div>
        <div className="sidebar">
            <SideBar/>
        </div>
        <div className="content">
            <Content/>    
        </div>
    </div>
    );
}

export default Home;