import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine
import tensorflow as tf
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import re

class FAQBot:
    def __init__(self, model_path='./faq_model', faq_path='processed_faq.csv'):
        # Load the trained model
        self.model = SentenceTransformer(model_path)
        
        # Load the processed FAQ data
        self.faq_df = pd.read_csv(faq_path)
        
        # Precompute embeddings for all questions
        self.question_embeddings = self.model.encode(
            self.faq_df['cleaned_question'].tolist(), 
            convert_to_tensor=True
        )
        
        # Initialize NLTK
        nltk.download('punkt')
        nltk.download('stopwords')
        self.stop_words = set(stopwords.words('english'))
    
    def clean_text(self, text):
        # Convert to string if not already
        text = str(text)
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        # Convert to lowercase
        text = text.lower()
        # Tokenize
        tokens = word_tokenize(text)
        # Remove stopwords and short tokens
        tokens = [word for word in tokens if word not in self.stop_words and len(word) > 2]
        return ' '.join(tokens)
    
    def _format_response(self, text, max_length=500):
        """Format the response text with line breaks and optional summarization"""
        # Add line breaks after periods for better readability
        text = text.replace('. ', '.\n\n')
        
        # If the text is too long, summarize it
        if len(text) > max_length:
            # Simple summarization by taking the first few sentences
            sentences = text.split('.')
            if len(sentences) > 3:
                summary = '.'.join(sentences[:3]) + '... [Response truncated. Ask for more details if needed.]'
                return summary
        return text
    
    def get_most_similar(self, query, top_k=3):
        # Clean and encode the query
        cleaned_query = self.clean_text(query)
        query_embedding = self.model.encode(cleaned_query, convert_to_tensor=True)
        
        # Calculate similarity with all questions
        similarities = []
        for i, q_embedding in enumerate(self.question_embeddings):
            # Calculate cosine similarity (1 - cosine distance)
            sim = 1 - cosine(query_embedding.cpu().numpy(), q_embedding.cpu().numpy())
            similarities.append((i, sim))
        
        # Sort by similarity score in descending order
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        # Get top-k most similar questions and answers
        results = []
        for idx, score in similarities[:top_k]:
            results.append({
                'question': self.faq_df.iloc[idx]['Questions'],
                'answer': self._format_response(self.faq_df.iloc[idx]['Answers']),
                'score': float(score)
            })
            
        return results

def main():
    # Load the model and data
    faq_bot = FAQBot()
    
    print("FAQ Bot is ready! Type 'quit' to exit.")
    print("-" * 50)
    
    try:
        while True:
            try:
                query = input("\nYou: ").strip()
                
                if query.lower() == 'quit':
                    print("Goodbye!")
                    break
                    
                if not query:
                    continue
                    
                # Get and display the most similar FAQs
                results = faq_bot.get_most_similar(query)
                
                if results and results[0]['score'] > 0.5:  # Threshold for considering a match
                    best_match = results[0]
                    print("\n" + "="*50)
                    print(f"FAQ Bot (Confidence: {best_match['score']*100:.1f}%):\n\n{best_match['answer']}")
                    print("="*50)
                    
                    # Show other possible matches if they exist
                    if len(results) > 1 and any(r['score'] > 0.3 for r in results[1:]):
                        print("\n" + "-"*50)
                        print("Did you also mean one of these?")
                        for i, result in enumerate(results[1:4], 1):
                            if result['score'] > 0.3:  # Only show reasonably good matches
                                print(f"\n{i}. {result['question']} (Confidence: {result['score']*100:.1f}%)")
                else:
                    print("\nFAQ Bot: I'm sorry, I don't have a good answer for that. Could you try rephrasing your question?")
                
            except EOFError:
                # Handle case when input is piped or redirected
                print("\nBot: Goodbye!")
                break
            except KeyboardInterrupt:
                print("\nBot: Goodbye!")
                break
            except Exception as e:
                print(f"\nBot: Sorry, I encountered an error: {str(e)}")
                continue
                
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return

if __name__ == "__main__":
    main()
