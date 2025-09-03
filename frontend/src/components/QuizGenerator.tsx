import React, { useState } from 'react';
import axios from 'axios';

interface Question {
  question: string;
  options: { [key: string]: string };
  correct: string;
}

const QuizGenerator: React.FC = () => {
  const [topic, setTopic] = useState('');
  const [questions, setQuestions] = useState<Question[]>([]);
  const [loading, setLoading] = useState(false);
  const [userAnswers, setUserAnswers] = useState<{ [key: number]: string }>({});
  const [showResults, setShowResults] = useState(false);

  const generateQuiz = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/generate-quiz', {
        topic,
        num_questions: 5
      });

      setQuestions(response.data?.questions ?? []);
      setUserAnswers({});
      setShowResults(false);
    } catch (error) {
      console.error('Quiz generation error:', error);
      setQuestions([]);
    } finally {
      setLoading(false);
    }
  };

  const submitQuiz = () => {
    setShowResults(true);
  };

  const calculateScore = () => {
    let correct = 0;
    questions.forEach((q, index) => {
      if (userAnswers[index] === q.correct) {
        correct++;
      }
    });
    return correct;
  };

  return (
    <div className="quiz-section">
      <h2>Generate Practice Quiz</h2>
      
      <div className="quiz-controls">
        <input
          type="text"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
          placeholder="Enter topic (optional)"
        />
        <button onClick={generateQuiz} disabled={loading}>
          {loading ? 'Generating...' : 'Generate Quiz'}
        </button>
      </div>

      {questions.length > 0 && (
        <div className="quiz-container">
          {questions.map((q, qIndex) => (
            <div key={qIndex} className="question-card">
              <h4>Question {qIndex + 1}: {q.question}</h4>
              
              {q.options && Object.entries(q.options).map(([letter, option]) => (
                <label key={letter} className="option-label">
                  <input
                    type="radio"
                    name={`question-${qIndex}`}
                    value={letter}
                    onChange={(e) =>
                      setUserAnswers({
                        ...userAnswers,
                        [qIndex]: e.target.value
                      })
                    }
                    disabled={showResults}
                  />
                  {letter}) {option}
                  {showResults && letter === q.correct && ' ✅'}
                  {showResults && letter === userAnswers[qIndex] && letter !== q.correct && ' ❌'}
                </label>
              ))}
            </div>
          ))}
          
          {!showResults ? (
            <button onClick={submitQuiz} className="submit-quiz-btn">
              Submit Quiz
            </button>
          ) : (
            <div className="quiz-results">
              <h3>Results: {calculateScore()}/{questions.length}</h3>
              <button onClick={() => setQuestions([])} className="new-quiz-btn">
                Generate New Quiz
              </button>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default QuizGenerator;