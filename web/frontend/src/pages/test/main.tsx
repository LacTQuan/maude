import React, { useState } from "react";
import "./main.css";

type File = {
  name: string;
  path: string;
};

const Test: React.FC = () => {
  const [initialState, setInitialState] = useState<string>("");
  const [pseudoCode, setPseudoCode] = useState<string>("");
  const [algo, setAlgo] = useState<string>("dijkstra");
  const [output, setOutput] = useState<string>("");
  const [options, setOptions] = useState<File[]>([]);
  const [algoOptions, _] = useState<File[]>([
    { name: "dijkstra", path: "../../maude_code/ogata/dijkstra/dijkstra00.maude" },
    { name: "astar", path: "../../maude_code/ogata/astar/astar00.maude" },
    { name: "lpastar", path: "../../maude_code/ogata/lpastar/lpastar00.maude" },
  ]);

  const getOptions = async () => {
    await fetch(`http://127.0.0.1:8000/list-files?directory=../../python/${algo}/test_cases`)
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
    // const algo = (document.getElementById("algorithm") as HTMLSelectElement)?.value;
    const algoPath = algoOptions.find((algoOption) => algoOption.name === algo)?.path;
    await fetch(`http://127.0.0.1:8000/run-maude?module=${algo.toUpperCase()}&algo_path=${algoPath}&test_case=` + test_case_path, {
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
  }, [algo]);


  return (
    <div className="container">
      <div className="dropdown">
        <label htmlFor="algorithm">Algorithm</label>
        <select id="algorithm" onChange={(e) => {
          setAlgo(e.target.value);
        }}>
          {algoOptions.map((algo) => (
            <option key={algo.name} value={algo.name}>
              {algo.name}
            </option>
          ))}
        </select>
      </div>
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
