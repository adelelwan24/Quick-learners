import Post from "./Post/Post";

const Content = () => {
    const logged_in = true

     // const {logged_in,posts} = useFetch('/recposts')
                
    return (
        <div>
        { logged_in && 
        <div>
            {/* {logged_in && posts.map(post=> <Post 
            query={post.query}  
            username={post.username}
            video_id={post.video_id}
            start={post.start}
            text={post.text}
            />)} */}

            <Post/>
            <Post/>
            <Post/>
        </div>
        }
        </div>
    );
}

export default Content;