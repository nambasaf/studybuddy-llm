import openai
import os
from typing import List


class LLMService:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def generate_answer(self, query: str, context_chunks: List[str], complexity: str = "medium") -> str:
        """Generate answer using OpenAI GPT"""

        # Adjust the system prompt based on complexity
        complexity_instructions = {
            "simple": "Explain in very simple terms, like you're talking to a high school student. Use analogies and everyday examples.",
            "medium": "Provide a clear explanation suitable for a college student. Include relevant details and examples.",
            "complex": "Give a comprehensive, technical explanation with detailed analysis and advanced concepts."
        }

        system_prompt = f"""You are an AI tutor helping students understand academic content.
        {complexity_instructions.get(complexity, complexity_instructions["medium"])}

        Use the provided context to answer the student's question. If the context doesn't contain
        enough information, say so and provide what general knowledge you can.
        """

        # Combine context chunks
        context = "\n\n".join(context_chunks)
        user_prompt = f"""Context from the document:
        {context}

        Student's question: {query}

        Please provide a helpful answer based on the context provided.
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # cheaper for me
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"
    
    def generate_quiz_questions(self, context_chunks: List[str], num_questions: int = 5) -> list[dict]:
        """Generate multiple choice quiz questions"""

        context = "\n\n".join(context_chunks[:3]) # first 3 chunks to avoid token limit
        prompt = f"""Based on the following text, create {num_questions} multiple questions.
        Each question should text understanding of key concepts. 
        Format each question as:
        Question: [question_text]
        A) [option A]
        B) [option B]  
        C) [option C]
        D) [option D]
        Correct Answer: [letter]

        Text: {context}"""

        try: 
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=800,
                temperature=0.8

            )
            # parse the response
            questions = self.parse_quiz_response(response.choices[0].message. content)  
            return questions
        except Exception as e:
            return [{"error": f"Could not generate quiz: {str(e)}"}]
        
    def _parse_quiz_response(self, response: str) -> List[dict]:
         """Parse quiz response into structured format"""
         questions = []
         current_question = {}
         lines = response.strip().split('\n')
         for line in lines:
             line = line.strip()
             if line.startswith('Question:'):
                 if current_question:
                     questions.append(current_question)
                 current_question = {'question': line[9:]. strip(), 'options': {}}
             elif line.startswith(('A)', 'B)', 'C)', 'D)')):
                 letter = line[0]
                 text = line[3:].strip()
                 current_question['options'][letter] = text
         if current_question:
             questions.append(current_question)

         return questions

