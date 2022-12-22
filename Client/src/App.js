import './App.css';
import {BrowserRouter ,Routes,Route} from 'react-router-dom' //react router
// import {Routes, Route} from 'react-router-dom' //react router

import Home from './Pages/Home/Home';
import Search from './Pages/Search/Search';
import SignIn from './Pages/SignIn/SignIn';
import SignUp from './Pages/SignUp/SignUp';

function App() {
  return (
    <BrowserRouter>
      <Routes>
          <Route path="/" element={ <Home/>}/>
          <Route path="/search" element={<Search />}/>
          <Route path="/signin" element={<SignIn />}/>
          <Route path="/signup" element={<SignUp />}/>
        </Routes>
    </BrowserRouter>
  );
}

export default App;
