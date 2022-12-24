import Post from "./Post/Post";
import UseFetch from "../../Methods/UseFetch";
import { useState, useEffect } from "react";
const Content = () => {
    const [loggedin , setLoggedin] = useState(false)
    let {data :data1, error1, isPending1} = UseFetch('/api/logged_in')
    // console.log(error)
    
    useEffect(() => {
        if(data1 == null){
            return
        }
        console.log(data1)
        setLoggedin(data1.logged_in)
    },[data1]);

    const [Posts, setPosts] = useState([])
    const {data , error , isPending} = UseFetch('/api/post_rec')
    useEffect(() => {
        if(data == null){
            return
        }
        setPosts(data.posts)
    },[data , data1])  
    
                
    return (

        <div>
            
                <p>because the website is still in development phase you can only search in these two playlists:</p>
                <div style={{"marginBottom":"35px"}}>
                    
                        <li>
                            <a href="https://www.youtube.com/playlist?list=PLUl4u3cNGP619EG1wp0kT-7rDE_Az5TNd">MIT 6.0002 Intro to Computational Thinking and Data Science</a>
                        </li>
                        <li>
                            <a href="https://www.youtube.com/playlist?list=PLUl4u3cNGP60uVBMaoNERc6knT_MgPKS0">MIT 18.650 Statistics for Applications, Fall 2016</a>
                        </li>
                    
                </div>
            
        { loggedin ?
        <div>
            {Posts && Posts.map(post=> <Post 
            key={post.query} 
            query={post.query}  
            video_id={post.video_id}
            start={post.start}
            text={post.text}
            />)} 
        </div>
            :
            (<div className="text-center" style={{'color':"gray"}}>
                sign up now to discover new posts 
            </div>)

            }
        </div>
    );
}

export default Content;




