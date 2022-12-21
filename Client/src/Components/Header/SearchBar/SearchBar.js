import { useNavigate } from "react-router-dom";
import { useState } from "react";
import Postmethod from "../../../Methods/PostMethod";

const SearchBar = () => {
    const navigate = useNavigate();
    
    const handleSubmit = async (event) => {
        event.preventDefault();
        let {err, resJson} = await Postmethod('/query',{query})
        console.log(resJson);
        navigate('/search', {state : {query , resJson}});
    }

    const [query , setQuery] = useState("");
    return ( 
    <form onSubmit={handleSubmit} id="queryform">
        <div className="input-group ">
            <input 
            type="text" 
            className="form-control" 
            placeholder="Search in videos" 
            aria-label="Search in videos" 
            aria-describedby="basic-addon2"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            required
            />
            <div className="input-group-append">
                <button className="btn btn-outline-secondary" type="submit">Search</button>
            </div>
        </div>
    </form>
    );
}

export default SearchBar;
