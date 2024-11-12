import React from "react";
import { Link, Route, Routes } from "react-router-dom";
import "./App.css";
import { Prompt } from "./pages/prompt";
import Test from "./pages/test/main";

const App: React.FC = () => {
  return (
    <div>
      <nav>
        <ul>
          <li><Link to="/prompt">Prompt</Link></li>
          <li><Link to="/test">Test</Link></li>
        </ul>
      </nav>
      <Routes>
        <Route path="/prompt" element={<Prompt />} />
        <Route path="/test" element={<Test />} />
      </Routes>
    </div>
  )
}

export default App;
