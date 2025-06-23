import { useEffect, useState } from "react";
// import axios from "axios";

function WordAnalysis(){
  const [category, setCategory] = useState("business");
  const [topWords, setTopWords] = useState([]);
  const [loading, setLoading] = useState(false);

  const categories = [
    "business",
    "entertainment",
    "lifestyle",
    "science",
    "sports",
    "health",
    "politics",
  ];

  useEffect(() => {
    const fetchTopWords = async () => {
      setLoading(true);
      try {
        const response = await fetch(
          `http://localhost:8000/top-words?category=${category}`
        );

        if (!response.ok) {
          throw new Error("Failed to fetch");
        }

        const data = await response.json();
        console.log(data);
        setTopWords(data || []);
        console.log(topWords);
      } catch (error) {
        console.error("Error fetching words:", error);
        setTopWords([]);
      } finally {
        setLoading(false);
      }
    };

    fetchTopWords();
  }, [category]);

  return (
		<div className="w-full min-h-full mx-auto p-4 border rounded-xl shadow bg-white text-stone-950 flex flex-col justify-start space-y-6">
      <h2 className="text-2xl font-semibold text-center">Analyze words by category</h2>

      <div className="flex justify-center">
        <select
          value={category}
          onChange={(e) => setCategory(e.target.value)}
          className="px-3 py-2 border rounded"
        >
          {categories.map((cat) => (
            <option key={cat} value={cat}>
              {cat}
            </option>
          ))}
        </select>
      </div>

      {loading ? (
        <p className="text-center text-gray-600">Loading...</p>
      ) : (
        <ul className="list-disc list-inside space-y-1 text-center max-h-[370px] overflow-y-auto">
          {topWords.map((item, idx) => (
            <li key={idx}>
              <span className="font-mono">{item.word}</span> — {item.count}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default WordAnalysis;