import { useState, useEffect } from 'react'

function ClassifierForm(){
    const [input, setInput] = useState("");
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
		e.preventDefault();
		if (!input.trim()) return;

		setLoading(true);
		setResult(null);

		try {
			const response = await fetch('http://localhost:8000/predict', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({ title: input }),
			});

			if (!response.ok) {
			throw new Error('Server error');
			}

			const data = await response.json();
			setResult(data);
		} catch (error) {
			console.error('Fetch error:', error);
			setResult({ error: 'Server error' });
		} finally {
			setLoading(false);
		}
	};


    return (
		<div className="w-full min-h-full mx-auto p-4 border rounded-xl shadow bg-white text-stone-950 flex flex-col justify-start space-y-6">
			<h2 className="text-2xl font-semibold text-center">Classification of the news</h2>

			<form onSubmit={handleSubmit} className="space-y-4">
				<input
				type="text"
				className="w-full border px-3 py-2 rounded"
				placeholder="Enter the news title"
				value={input}
				onChange={(e) => setInput(e.target.value)}
				/>

				<button
				type="submit"
				className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition"
				disabled={loading}
				>
				{loading ? "Classification..." : "Classify"}
				</button>
			</form>

			{result?.predicted_category && (
				<div className="text-center space-y-4">
				<p className="text-lg">
					Predicted category: <strong>{result.predicted_category}</strong>
				</p>

				{result.probabilities && (
					<div className="mt-2">
					<p className="font-medium mb-2">Category probabilities:</p>
					<ul className="space-y-1 text-center">
						{Object.entries(result.probabilities).map(([category, prob]) => (
							<li key={category}>
							<span className="font-mono">{category}</span>: {(prob * 100).toFixed(2)}%
							</li>
						))}
					</ul>
					</div>
				)}
				</div>
			)}

			{result?.error && (
				<p className="text-red-600 text-center">{result.error}</p>
			)}
		</div>
    );
}

export default ClassifierForm;