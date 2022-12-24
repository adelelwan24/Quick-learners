import SiteName from "../../Components/Header/SiteName/SiteName";
import  { useState  } from 'react';
import Postmethod from "../../Methods/PostMethod";
import { useNavigate } from "react-router-dom";


const SignUp = () => {
    const navigate = useNavigate();
    const [email , setEmail] = useState('')
    const [message , setMessage] = useState('')
    const [name , setName] = useState('')
    const [username , setUsername] = useState('')
    const [password , setPassword] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();
        let {err, resJson} = await Postmethod('/api/register',{name,username, email,password})
        console.log(err)
        if(resJson.logged_in == true){
            navigate('/');
        }
        else{
            setMessage("username or email address is taken")
        }
        
        //svae cart to user cart in data base 
        //compare my cart to user cart and update and delete local storage
        //save the result in cart state
        // let response1 = await fetch('/api/auth/verifyUser');
        // console.log(response1);
        // if (response1.ok){
        //     setUser("true");
        // }
        // else{
        //     setUser("false");
        // }

            
        

        }
    return (
        <>
        <div style={{"margin-top":"20px" ,"margin-left":"50px" }}>
            <SiteName   />
        </div>
        
        {/* <Header style={{"margin-top":"50px"}}/> */}
        <form onSubmit={handleSubmit} style={{"width":"25%"  , "height":"30%" , "margin":"auto" ,"margin-top":"5%"}}>
            <div className="form-outline mb-4">
                <input 
                type="text" 
                id="form2Example1" 
                className="form-control"
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
                placeholder="Name"
                />  
            </div>
            <div className="form-outline mb-4">
                <input 
                type="text" 
                id="form2Example1" 
                className="form-control"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                placeholder="Username"
                />  
            </div>
            <div className="form-outline mb-4">
                <input 
                type="email" 
                id="form2Example1" 
                className="form-control"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                placeholder="Email"
                />  
            </div>

            <div className="form-outline mb-4">
                <input 
                type="password" 
                id="form2Example2" 
                className="form-control"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                placeholder="Password" 
                />
            </div>

            <button className="btn btn-primary btn-block mb-4" type="submit">Sign up</button>

            <div className="text-center">
                <p>Already a member? <a href="/signin">sign in</a></p>
            </div>
            <div className="text-center">
                <span  style={{'color':"red" , "fontSize":"12px" }}>{message}</span>
            </div>
        </form>
        </>
    );
}
 
export default SignUp;