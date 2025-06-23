import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import ClassifierForm from "./components/ClassifierForm.jsx"
import WordAnalysis from "./components/WordAnalysis.jsx"
import './App.css'

function App() {
  const [mode, setMode] = useState("classifier");

  return (
    <div className="bg-gray-100 flex items-center justify-center rounded-xl ">
      <div className="w-full max-w-3xl bg-white rounded-2xl shadow-xl p-6 min-h-[700px] min-w-[500px] flex flex-col ">
        
        <h1 className="text-3xl font-bold text-center mb-6 text-gray-800">
          News Classifier
        </h1>

        <div className="flex justify-center gap-4 mb-6">
          <button
            onClick={() => setMode("classifier")}
            className={`px-4 py-2 rounded-xl font-medium transition ${
              mode === "classifier"
                ? "bg-blue-600 text-white"
                : "bg-gray-200 text-gray-800 hover:cursor-pointer"
            }`}
          >
            Classifier
          </button>

          <button
            onClick={() => setMode("analysis")}
            className={`px-4 py-2 rounded-xl font-medium transition ${
              mode === "analysis"
                ? "bg-blue-600 text-white"
                : "bg-gray-200 text-gray-800 hover:cursor-pointer"
            }`}
          >
            Word analysis
          </button>
        </div>

        <div className="flex-1 flex font-medium">
          {mode === "classifier" && <ClassifierForm />}
          {mode === "analysis" && <WordAnalysis />}
        </div>
      </div>
    </div>
  );
}
export default App
