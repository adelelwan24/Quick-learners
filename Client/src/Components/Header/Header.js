import SearchBar from "./SearchBar/SearchBar";
import NotSigned from "./NotSigned/NotSigned";
import SiteName from "./SiteName/SiteName";
const Header = () => {
    return ( 
        <div className="header-me">
            <div className="header-me-1">
                <SiteName/>
            </div>
            <div className="header-me-2">
                <SearchBar/>
            </div>
            <div className="header-me-3">
                <NotSigned/>
            </div>
            
        </div>
    );
}

export default Header;