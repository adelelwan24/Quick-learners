import Content from "../../Components/Content/Content";
import Header from "../../Components/Header/Header";
import SideBar from "../../Components/SideBar/SideBar";
const Home = () => {
    return ( 
    <div class="container-me">
        <div class="header">
            <Header/>
        </div>
        <div class="sidebar">
            <SideBar/>
        </div>
        <div class="content">
            <Content/>    
        </div>
    </div>
    );
}

export default Home;