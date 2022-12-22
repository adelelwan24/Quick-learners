import Post from "./Post/Post";
import UseFetch from "../../Methods/UseFetch";
import { useState, useEffect } from "react";
const Content = () => {

    const [logged_in, setLogged_in] = useState(false)
    const [Posts, setPosts] = useState([])
    const {data , error , isPending} = UseFetch('/api/post_rec')
    useEffect(() => {
        if(data == null){
            return
        }
        setLogged_in(data.logged_in)
        setPosts(data.posts)
    },[data])  
    
                
    return (
        <div>
        { logged_in && 
        <div>
            {Posts && Posts.map(post=> <Post 
            query={post.query}  
            video_id={post.video_id}
            start={post.start}
            text={post.text}
            />)}
        </div>
        }
        </div>
    );
}

export default Content;




