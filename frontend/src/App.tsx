import  { useState } from 'react';
import FileUpload from './components/FileUpload';
import QuestionAsker from './components/QuestionAsker';
import QuizGenerator from './components/QuizGenerator';
import './App.css';


export default function App() {
  const [uploadedDoc, setUploadedDoc] = useState<string | null>(null);

  return (
    <div className="App">
      <header className="App-header">
        <h1>📚 StudyBuddy</h1>
        <p>Your AI-powered learning assistant</p>
      </header>

      <main className="main-content">
         <FileUpload onUploadSuccess={setUploadedDoc} />
        
        {uploadedDoc && (
          <>
            <QuestionAsker />
            <QuizGenerator />
          </>
        )}
      </main>
    </div>
  )
}
