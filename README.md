# Mental Health FAQ Chatbot

This project implements a conversational FAQ bot for mental health questions using sentence transformers and TFLite. The bot can understand natural language questions and provide relevant answers from a knowledge base of mental health FAQs.

## Project Structure

- `train_faq_bot.py`: Script to preprocess the FAQ data and train the model
- `faq_bot.py`: Interactive script to chat with the trained FAQ bot
- `Mental_Health_FAQ.csv`: The input FAQ dataset
- `requirements.txt`: Python dependencies
- `faq_model/`: Directory containing the trained model (created after training)
- `processed_faq.csv`: Preprocessed FAQ data (created after training)

## Setup

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Download NLTK data (if not already downloaded):
   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('stopwords')
   ```

## Training the Model

To train the FAQ bot, run:

```bash
python train_faq_bot.py
```

This will:
1. Preprocess the FAQ data
2. Train a sentence transformer model
3. Save the model in the `faq_model` directory
4. Create a TFLite model (`faq_model.tflite`)

## Running the FAQ Bot

To start an interactive session with the FAQ bot, run:

```bash
python faq_bot.py
```

Type your questions about mental health, and the bot will try to provide relevant answers from its knowledge base.

## How It Works

1. The system uses a pre-trained sentence transformer model (`all-MiniLM-L6-v2`) fine-tuned on the mental health FAQ data.
2. When a user asks a question, the system:
   - Cleans and preprocesses the input text
   - Converts it to a vector embedding
   - Finds the most similar questions in the FAQ database using cosine similarity
   - Returns the most relevant answers

## Model Conversion to TFLite

The trained model is converted to TFLite format for efficient deployment on mobile and embedded devices. The conversion process:
1. Saves the PyTorch model
2. Converts it to ONNX format
3. Converts ONNX to TFLite

The final TFLite model is saved as `faq_model.tflite`.

## Customization

To customize the FAQ bot with your own data:
1. Replace `Mental_Health_FAQ.csv` with your own FAQ data in the same format
2. Update the training parameters in `train_faq_bot.py` if needed
3. Retrain the model

## License

This project is for educational purposes only. Please ensure you have the right to use the FAQ data for your specific use case.
