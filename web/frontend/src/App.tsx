import React, { useState } from "react";
import "./App.css";
import axios from "axios";

const App: React.FC = () => {
  const [initialState, setInitialState] = useState<string>("");
  const [pseudoCode, setPseudoCode] = useState<string>("");
  const [output, setOutput] = useState<string>("");
  const [options, setOptions] = useState<{}>([]);

  const getOptions = async () => {
    console.log("Fetching options");
    // no cors fetching, add mode: 'no-cors' to the request
    await fetch("http://localhost:8000/list-files?directory=../../maude_code", {
      method: "GET",
      mode: "no-cors",
    })
      .then((response) => {
        console.log("Response:", response);
        return response.json();
      })
      .then((data) => {
        console.log("Data:", data);
        setOptions(data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  React.useEffect(() => {
    getOptions();
  }, []);

  const handleSubmit = () => {
    // Handle submit logic
    console.log("Submitted:", { initialState, pseudoCode, output });
  };

  return (
    <div className="container">
      <div className="dropdown">
        <label htmlFor="maudeCode">Maude code</label>
        <select id="maudeCode">
          {options.map((option: string) => (
            <option key={option} value={option}>
              {option}
            </option>
          ))}
        </select>
      </div>

      <div className="inputSection">
        <div className="textareaContainer">
          <label htmlFor="initialState">Initial state</label>
          <textarea
            id="initialState"
            value={initialState}
            onChange={(e) => setInitialState(e.target.value)}
          />
        </div>

        <div className="textareaContainer">
          <label htmlFor="pseudoCode">Pseudo code</label>
          <textarea
            id="pseudoCode"
            value={pseudoCode}
            onChange={(e) => setPseudoCode(e.target.value)}
          />
        </div>
      </div>

      <div className="textareaContainer inputSection">
        <div className="outputContainer">
          <label htmlFor="output">Output</label>
          <textarea
            id="output"
            value={output}
            onChange={(e) => setOutput(e.target.value)}
          />
        </div>
      </div>

      <button className="submitButton" onClick={handleSubmit}>
        Submit
      </button>
    </div>
  );
};

export default App;
