import './App.css';
import {BrowserRouter ,Routes,Route} from 'react-router-dom' //react router
// import {Routes, Route} from 'react-router-dom' //react router

import Home from './Pages/Home/Home';
import Search from './Pages/Search/Search';

function App() {
  return (
    <BrowserRouter>
      <Routes>
          <Route path="/" element={ <Home/>}/>
          <Route path="/search" element={<Search />}/>
        </Routes>
    </BrowserRouter>
  );
}

export default App;
