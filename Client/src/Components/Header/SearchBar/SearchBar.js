const SearchBar = () => {
    return ( 
    <div className="input-group ">
        <input type="text" className="form-control" placeholder="Search in videos" aria-label="Search in videos" aria-describedby="basic-addon2"/>
        <div className="input-group-append">
            <button className="btn btn-outline-secondary" type="button">Search</button>
        </div>
    </div>
    );
}

export default SearchBar;

