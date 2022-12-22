const UserCart = ({name,usernaem}) => {
    return (
    <div className="card-me card" >
        <div>
            <span className="card-title">name</span>
            <br></br>
            <span style={{color: "grey"}} className="card-text"><span>@</span>username</span>

            {/* <span className="card-title">{name}</span>
            <br></br>
            <span style={{color: "grey"}} className="card-text"><span>@</span>{username}</span> */}
        </div>
        <div >
            <a href="#" className="card-link">Connect</a>
            <a href="#" className="card-link">Add to Group</a>
        </div>
    </div>
    );
}

export default UserCart;