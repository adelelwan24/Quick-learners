const QueryAnswer = ({id,start}) => {
    return (
        <div className="card post-me">
            <div className="card-body">
                <p className="card-text">answer of the querie from the video</p>
            </div>
            <div className="embed-responsive embed-responsive-16by9">
                <iframe className="embed-responsive-item" src={`https://www.youtube.com/embed/${id}?start=${start}`} allowFullScreen></iframe>
            </div>
        </div>
    );
}

export default QueryAnswer;
