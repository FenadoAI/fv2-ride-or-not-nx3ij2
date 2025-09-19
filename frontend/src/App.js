import { useEffect, useState } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import axios from "axios";

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8001';
const API = `${API_BASE}/api`;

const CarRating = () => {
  const [currentCar, setCurrentCar] = useState(null);
  const [loading, setLoading] = useState(true);
  const [showScore, setShowScore] = useState(false);
  const [lastVoteResult, setLastVoteResult] = useState(null);
  const [voting, setVoting] = useState(false);

  const fetchRandomCar = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API}/cars/random`);
      setCurrentCar(response.data);
      setShowScore(false);
      setLastVoteResult(null);
    } catch (error) {
      console.error("Error fetching car:", error);
    } finally {
      setLoading(false);
    }
  };

  const vote = async (voteType) => {
    if (!currentCar || voting) return;

    try {
      setVoting(true);
      const response = await axios.post(`${API}/cars/vote`, {
        car_id: currentCar.id,
        vote_type: voteType
      });

      setLastVoteResult(response.data.car);
      setShowScore(true);

      // Show score for 3 seconds then load next car
      setTimeout(() => {
        fetchRandomCar();
      }, 3000);
    } catch (error) {
      console.error("Error voting:", error);
      setVoting(false);
    }
  };

  useEffect(() => {
    fetchRandomCar();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <div className="text-white text-2xl">Loading...</div>
      </div>
    );
  }

  if (showScore && lastVoteResult) {
    return (
      <div className="min-h-screen bg-gray-900 flex flex-col items-center justify-center p-8">
        <div className="max-w-2xl w-full text-center">
          <div className="mb-8">
            <img
              src={lastVoteResult.image_url}
              alt={`${lastVoteResult.year} ${lastVoteResult.make} ${lastVoteResult.model}`}
              className="w-full h-96 object-cover rounded-lg shadow-lg"
            />
          </div>

          <h2 className="text-3xl font-bold text-white mb-4">
            {lastVoteResult.year} {lastVoteResult.make} {lastVoteResult.model}
          </h2>

          <div className="bg-gray-800 rounded-lg p-6 mb-6">
            <div className="text-4xl font-bold text-green-400 mb-2">
              {lastVoteResult.hot_percentage}% Hot
            </div>
            <div className="text-gray-300">
              {lastVoteResult.hot_votes} Hot • {lastVoteResult.not_votes} Not • {lastVoteResult.total_votes} Total Votes
            </div>
          </div>

          <div className="text-gray-400">
            Loading next car...
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-900 flex flex-col items-center justify-center p-8">
      <div className="max-w-2xl w-full text-center">
        <h1 className="text-4xl font-bold text-white mb-8">Car Rater</h1>

        {currentCar && (
          <>
            <div className="mb-8">
              <img
                src={currentCar.image_url}
                alt={`${currentCar.year} ${currentCar.make} ${currentCar.model}`}
                className="w-full h-96 object-cover rounded-lg shadow-lg"
              />
            </div>

            <h2 className="text-2xl font-bold text-white mb-8">
              {currentCar.year} {currentCar.make} {currentCar.model}
            </h2>

            <div className="flex gap-8 justify-center">
              <button
                onClick={() => vote('hot')}
                disabled={voting}
                className="bg-red-500 hover:bg-red-600 disabled:opacity-50 text-white font-bold py-4 px-8 rounded-lg text-xl transition-colors"
              >
                🔥 Hot
              </button>

              <button
                onClick={() => vote('not')}
                disabled={voting}
                className="bg-blue-500 hover:bg-blue-600 disabled:opacity-50 text-white font-bold py-4 px-8 rounded-lg text-xl transition-colors"
              >
                ❄️ Not
              </button>
            </div>

            {voting && (
              <div className="mt-4 text-gray-400">
                Recording your vote...
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<CarRating />}>
            <Route index element={<CarRating />} />
          </Route>
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
