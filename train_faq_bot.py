import os
import re
import json
import numpy as np
import pandas as pd
from tqdm import tqdm
from typing import List, Tuple, Dict, Any
import nltk
import ssl

# Download required NLTK data
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
    nltk.data.find('tokenizers/punkt_tab')
    nltk.data.find('corpora/wordnet')
except LookupError:
    print("Downloading NLTK data...")
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt_tab', quiet=True)
    nltk.download('wordnet', quiet=True)

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string
from sentence_transformers import SentenceTransformer, InputExample, losses, evaluation
from torch.utils.data import DataLoader
import tensorflow as tf
from tensorflow import keras
import tensorflow_hub as hub
import re
import os
from tqdm import tqdm

class FAQPreprocessor:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        
    def clean_text(self, text: str) -> str:
        try:
            # Convert to string if not already
            text = str(text)
            # Convert to lowercase
            text = text.lower()
            # Remove punctuation
            text = text.translate(str.maketrans('', '', string.punctuation))
            # Tokenization with error handling
            try:
                tokens = word_tokenize(text)
            except LookupError:
                nltk.download('punkt')
                tokens = word_tokenize(text)
            
            # Remove stopwords with error handling
            try:
                stop_words = set(stopwords.words('english'))
            except LookupError:
                nltk.download('stopwords')
                stop_words = set(stopwords.words('english'))
                
            tokens = [word for word in tokens if word not in stop_words]
            
            # Lemmatization with error handling
            try:
                lemmatizer = WordNetLemmatizer()
            except LookupError:
                nltk.download('wordnet')
                lemmatizer = WordNetLemmatizer()
                
            tokens = [lemmatizer.lemmatize(word) for word in tokens]
            # Join tokens back to string
            return ' '.join(tokens)
        except Exception as e:
            print(f"Error in clean_text: {str(e)}")
            return str(text)  # Return original text if cleaning fails

class FAQModel:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name)
        self.preprocessor = FAQPreprocessor()
        
    def prepare_data(self, df):
        """Prepare training data from the FAQ dataframe"""
        # Clean questions and answers
        df['cleaned_question'] = df['Questions'].apply(self.preprocessor.clean_text)
        df['cleaned_answer'] = df['Answers'].apply(self.preprocessor.clean_text)
        
        # Create training examples
        train_examples = []
        for _, row in df.iterrows():
            train_examples.append(InputExample(
                texts=[row['cleaned_question'], row['cleaned_answer']],
                label=1.0  # Positive pair
            ))
        
        return train_examples, df
    
    def train(self, train_examples, output_dir='faq_model', num_epochs=3, batch_size=16):
        """Train the model on the given examples"""
        print("Training the model...")
        
        # Create DataLoader
        train_dataloader = DataLoader(train_examples, shuffle=True, batch_size=batch_size)
        
        # Define the loss
        train_loss = losses.MultipleNegativesRankingLoss(model=self.model)
        
        # Train the model
        self.model.fit(
            train_objectives=[(train_dataloader, train_loss)],
            epochs=num_epochs,
            show_progress_bar=True
        )
        
        # Save the model
        self.model.save(output_dir)
        print(f"Model saved to {output_dir}")
        
        # Skip TFLite conversion for now
        print("Skipping TFLite conversion. The model is saved in a format ready for inference.")
        return self.model
    
    def _convert_to_onnx(self, output_dir='faq_model/onnx'):
        """Convert the model to ONNX format for mobile deployment"""
        try:
            import os
            import torch
            from transformers import AutoModel, AutoTokenizer
            import onnx
            import onnxruntime as ort
            
            print("Converting model to ONNX format...")
            
            # Create output directory
            os.makedirs(output_dir, exist_ok=True)
            
            # Load the model and tokenizer
            model_name = 'sentence-transformers/all-MiniLM-L6-v2'
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModel.from_pretrained(model_name)
            
            # Save tokenizer
            tokenizer.save_pretrained(output_dir)
            
            # Create dummy input
            dummy_input = tokenizer("This is a test", return_tensors="pt")
            
            # Define input and output names
            input_names = ["input_ids", "attention_mask"]
            output_names = ["last_hidden_state"]
            
            # Set dynamic axes for variable length inputs
            dynamic_axes = {
                'input_ids': {0: 'batch', 1: 'sequence'},
                'attention_mask': {0: 'batch', 1: 'sequence'},
                'last_hidden_state': {0: 'batch', 1: 'sequence'}
            }
            
            # Export the model to ONNX with opset 14 for scaled_dot_product_attention support
            onnx_path = os.path.join(output_dir, 'model.onnx')
            torch.onnx.export(
                model,
                (dummy_input['input_ids'], dummy_input['attention_mask']),
                onnx_path,
                input_names=input_names,
                output_names=output_names,
                dynamic_axes=dynamic_axes,
                opset_version=14,  # Updated to support scaled_dot_product_attention
                export_params=True,
                do_constant_folding=True,
                verbose=True
            )
            
            # Verify the ONNX model
            onnx_model = onnx.load(onnx_path)
            onnx.checker.check_model(onnx_model)
            
            # Test the ONNX model
            ort_session = ort.InferenceSession(onnx_path)
            ort_inputs = {
                'input_ids': dummy_input['input_ids'].numpy(),
                'attention_mask': dummy_input['attention_mask'].numpy()
            }
            ort_outs = ort_session.run(None, ort_inputs)
            
            print(f"ONNX model saved to {onnx_path}")
            print("ONNX model test successful!")
            
            # Create a simple text file with model info
            with open(os.path.join(output_dir, 'model_info.txt'), 'w') as f:
                f.write(f"Model: {model_name}\n")
                f.write(f"Input names: {input_names}\n")
                f.write(f"Output names: {output_names}\n")
                f.write("\nTo use this model in Android, use ONNX Runtime for Android.\n")
                f.write("The tokenizer directory contains the necessary files for text preprocessing.")
            
            return onnx_path
            
        except Exception as e:
            print(f"Error converting to ONNX: {str(e)}")
            print("Falling back to PyTorch model only.")
            return None

def main():
    # Load the FAQ data
    df = pd.read_csv('Mental_Health_FAQ.csv')
    
    # Initialize and train the model
    faq_model = FAQModel()
    
    # Prepare data
    print("Preparing training data...")
    train_examples, processed_df = faq_model.prepare_data(df)
    
    # Save processed data for reference
    processed_df.to_csv('processed_faq.csv', index=False)
    
    # Train the model
    print("Training the model...")
    model = faq_model.train(
        train_examples,
        output_dir='./faq_model',
        num_epochs=3,
        batch_size=16
    )
    
    print("Training completed!")
    
    # Convert to ONNX
    onnx_path = faq_model._convert_to_onnx()
    if onnx_path:
        print(f"Model successfully converted to ONNX format: {onnx_path}")
        print("\nTo use this model in Android:")
        print("1. Add ONNX Runtime for Android to your project")
        print("2. Copy the 'onnx' directory to your Android assets folder")
        print("3. Use the saved tokenizer for text preprocessing")
        print("4. Load and run the ONNX model with ONNX Runtime")
    else:
        print("Could not convert model to ONNX format. Using standard PyTorch model.")
    
    print("All operations completed!")

if __name__ == "__main__":
    main()
