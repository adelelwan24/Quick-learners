import SiteName from "../../Components/Header/SiteName/SiteName";
import  { useState  } from 'react';
import Postmethod from "../../Methods/PostMethod";

const SignIn = () => {
    const [email , setEmail] = useState('')
    const [password , setPassword] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();
        let {err, mess} = await Postmethod('/auth/login',{email,password})
        
        
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

            <button className="btn btn-primary btn-block mb-4" type="submit">Sign in</button>

            <div className="text-center">
                <p>Not a member? <a href="/signup">Register</a></p>
            </div>
        </form>
        </>
    );
}
 
export default SignIn;