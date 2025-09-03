import React, { useState } from 'react';
import axios from 'axios';

const QuestionAsker: React.FC = () => {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [complexity, setComplexity] = useState('medium');
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    if (!question.trim()) return;

    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/ask', {
        question,
        complexity
      });

      setAnswer(response.data.answer);
    } catch (error) {
      setAnswer('Sorry, I encountered an error while processing your question.');
      console.error('Question error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="question-section">
      <h2>Ask Questions</h2>
      
      <div className="complexity-selector">
        <label>Explanation Level:</label>
        <select value={complexity} onChange={(e) => setComplexity(e.target.value)}>
          <option value="simple">Simple</option>
          <option value="medium">Medium</option>
          <option value="complex">Complex</option>
        </select>
      </div>

      <div className="question-input">
        <textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask any question about your uploaded document..."
          rows={3}
        />
        <button onClick={askQuestion} disabled={loading || !question.trim()}>
          {loading ? 'Thinking...' : 'Ask Question'}
        </button>
      </div>

      {answer && (
        <div className="answer-box">
          <h3>Answer:</h3>
          <p>{answer}</p>
        </div>
      )}
    </div>
  );
};

export default QuestionAsker;