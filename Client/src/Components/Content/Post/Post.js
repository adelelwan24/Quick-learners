const Post = () => {
    return (
        <div className="card post-me"   >
            
            <div className="card-body">
                <h5 className="card-title">query from <span style={{color: "grey"}} className="card-text"><span>@</span>username</span></h5>
                <p className="card-text">answer of the querie from the video</p>
            </div>
            <div className="embed-responsive embed-responsive-16by9">
                <iframe className="embed-responsive-item" src="https://www.youtube.com/embed/V_TulH374hw?rel=0" allowfullscreen></iframe>
            </div>
        </div>
    );
}

export default Post;