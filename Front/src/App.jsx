import { useState, useEffect } from "react";

import axios from "axios";
import Editor from "@monaco-editor/react";


import "./index.css";
const API_URL=import.meta.env.VITE_API_URL;

function App() {

  const [code, setCode] = useState(
`let x = 5;
print(x + 10);`
  );

  const [result, setResult] = useState(null);

  const [history, setHistory] = useState([]);


  const executeCode = async () => {

    try {

      const response = await axios.post(
        `${API_URL}/execute`,
       // "http://127.0.0.1:8000/execute",
        {
          code: code
        }
      );

      setResult(response.data);

    } catch (error) {

      console.error(error);

      if (error.response) {

        setResult({
          error: error.response.data
        });

      } else {

        setResult({
          error: error.message
        });
      }
    }
  };


  const saveExecution = async () => {

    try {

      const response = await axios.post(
       // "http://127.0.0.1:8000/save",
       `${API_URL}/execute`,
        {
          code: code
        }
      );

      alert(response.data.message);

      loadHistory();

    } catch (error) {

      console.error(error);
    }
  };

  const loadHistory = async () => {

    try {

      const response = await axios.get(
        //"http://127.0.0.1:8000/history"
        `${API_URL}/execute`
      );

      setHistory(response.data);

    } catch (error) {

      console.error(error);
    }
  };

  useEffect(() => {

    loadHistory();

  }, []);

  // =========================
  // CARGAR EJECUCIÓN
  // =========================

  const loadExecution = async (savedCode) => {

    setCode(savedCode);

    try {

      const response = await axios.post(
`${API_URL}/execute`,
        //"http://127.0.0.1:8000/execute",
        {
          code: savedCode
        }
      );

      setResult(response.data);

    } catch (error) {

      console.error(error);
    }
  };

  return (

    <div className="container">

      <h1 className="title">
        MathLite IDE
      </h1>

      {/* ========================= */}
      {/* EDITOR */}
      {/* ========================= */}

      <div className="editor-container">

        <Editor
          height="400px"
          defaultLanguage="javascript"
          theme="vs-dark"
          value={code}
          onChange={(value) => setCode(value)}
        />

      </div>


      <div
        style={{
          display: "flex",
          gap: "10px",
          marginTop: "20px"
        }}
      >

        <button
          className="button"
          onClick={executeCode}
        >
          Ejecutar
        </button>

        <button
          className="button"
          onClick={saveExecution}
        >
          Guardar
        </button>

        <button
          className="button"
          onClick={loadHistory}
        >
          Historial
        </button>

      </div>

      {result && (

        <div className="result">

          <h2>
            Resultado
          </h2>

          <pre>
            {JSON.stringify(result, null, 2)}
          </pre>

        </div>
      )}


      <div className="result">

        <h2>
          Historial
        </h2>

        {

          history.map((item, index) => (

            <div
              key={index}
              onClick={() =>
                loadExecution(item.code)
              }
              style={{
                border: "1px solid gray",
                padding: "10px",
                marginBottom: "10px",
                cursor: "pointer"
              }}
            >

              <strong>
                Consulta #{index + 1}
              </strong>

              <pre>
                {item.code}
              </pre>

            </div>
          ))
        }

      </div>

    </div>
  );
}

export default App;