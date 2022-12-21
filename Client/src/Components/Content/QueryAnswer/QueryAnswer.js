const QueryAnswer = ({id,start,text}) => {
    console.log(start)
    return (
        <div className="card post-me">
            <div className="card-body">
                <h6>Match:</h6>
                <p className="card-text">{text}</p>
            </div>
            <div className="embed-responsive embed-responsive-16by9">
                <iframe className="embed-responsive-item" src={`https://www.youtube.com/embed/${id}?start=${Math.floor(start)}`} allowFullScreen></iframe>
            </div>
        </div>
    );
}

export default QueryAnswer;
