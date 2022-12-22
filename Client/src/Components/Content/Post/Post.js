const Post = ({query,username,video_id,start,text}) => {
    return (
        <div className="card post-me">
            <div className="card-body">
                <h5 className="card-title">query from <span style={{color: "grey"}} className="card-text"><span>@</span>username</span></h5>
                <p className="card-text">answer of the querie from the video</p>
            </div>
            <div className="embed-responsive embed-responsive-16by9">
                <iframe className="embed-responsive-item" src="https://www.youtube.com/embed/V_TulH374hw?rel=0" allowFullScreen></iframe>
            </div>

            {/* <div className="card-body">
                <h6 className="card-title">query from <span style={{color: "grey"}} className="card-text"><span>@</span>{username}</span></h6>
                <p className="card-text">query: {query}</p>
                <p className="card-text">{text}</p>
            </div>
            <div className="embed-responsive embed-responsive-16by9">
                <iframe className="embed-responsive-item" src={`https://www.youtube.com/embed/${video_id}?start=${Math.floor(start)}`} allowFullScreen></iframe>
            </div> */}
        </div>
    );
}


export default Post;