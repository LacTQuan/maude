import React, { useState } from "react";
import "./main.css";

type File = {
  name: string;
  path: string;
};

const Test: React.FC = () => {
  const [initialState, setInitialState] = useState<string>("");
  const [pseudoCode, setPseudoCode] = useState<string>("");
  const [output, setOutput] = useState<string>("");
  const [options, setOptions] = useState<File[]>([]);

  const getOptions = async () => {
    await fetch("http://127.0.0.1:8000/list-files?directory=../../python/dijkstra/test_cases")
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        const files = data.files.map((file: File) => {
          return {
            name: file.name,
            path: file.path,
          };
        });
        setOptions(files);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  };

  const handleSubmit = async () => {
    const test_case_path = (document.getElementById("testCase") as HTMLSelectElement)?.value;
    await fetch("http://127.0.0.1:8000/run-maude?test_case=" + test_case_path, {
      method: "GET",
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        const results = data.results;
        console.log(results);
        setOutput("");
        for (let i = 0; i < results.length; i++) {
          const testTitle = results[i].test_title;
          const solution = results[i].solution ? results[i].solution : results[i].error;
          setOutput((prevOutput) => prevOutput + testTitle + "\n" + solution + "\n\n");
        }
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }

  React.useEffect(() => {
    getOptions();
  }, []);


  return (
    <div className="container">
      <div className="dropdown">
        <label htmlFor="testCase">Test cases</label>
        <select id="testCase">
          {options.map((file) => (
            <option key={file.path} value={file.path}>
              {file.name}
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
            disabled
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

export default Test;
