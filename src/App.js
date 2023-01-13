import React from 'react';
import { BrowserRouter as Router, Routes, Route }
    from 'react-router-dom';
import SearchRoute from './pages/index.js';
import BestRoutes from './pages/bestRoutes';
import './styles/App.css';

function App() {

    return (
        <Router>
            <div id='main-container'>
                <Routes>
                    <Route path='/' element={<SearchRoute />} />
                    <Route path='/bestRoutes' element={<BestRoutes />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;