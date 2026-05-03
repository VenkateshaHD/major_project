import torch
from transformers import BertTokenizer, BertForSequenceClassification
import os

class ModelService:
    def __init__(self, model_dir="backend/model_save"):
        self.model_dir = model_dir
        self.model = None
        self.tokenizer = None
        # In a real scenario we use GPU if available, but requirements specify CPU fallback
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.load_model()

    def load_model(self):
        """
        Loads the trained BERT model and tokenizer from the model directory.
        If the directory doesn't exist, it loads the pre-trained bert-base-uncased
        as a fallback (mostly to ensure the app runs out-of-the-box before training).
        """
        if os.path.exists(self.model_dir):
            try:
                self.tokenizer = BertTokenizer.from_pretrained(self.model_dir)
                self.model = BertForSequenceClassification.from_pretrained(self.model_dir)
                print(f"Model loaded from {self.model_dir}")
            except Exception as e:
                print(f"Error loading model from {self.model_dir}: {e}")
                self._load_fallback()
        else:
            print(f"Model directory {self.model_dir} not found. Loading fallback model.")
            self._load_fallback()
            
        self.model.to(self.device)
        self.model.eval()

    def _load_fallback(self):
        """Loads a base model for demonstration if fine-tuned model isn't available."""
        self.tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
        # 2 labels: 0 -> Genuine, 1 -> Fake
        self.model = BertForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=2)
        print("Fallback bert-base-uncased loaded.")

    def predict(self, text: str):
        """
        Tokenizes the input text, passes it through the model,
        and returns the predicted class and confidence.
        """
        # Tokenize input
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        # Predict
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            
        # Apply softmax to get probabilities
        probabilities = torch.nn.functional.softmax(logits, dim=-1)
        
        # Get highest prob class
        predicted_class_id = torch.argmax(probabilities, dim=-1).item()
        confidence = probabilities[0][predicted_class_id].item()

        # Map to label (0 -> Genuine, 1 -> Fake) based on notebook logic
        label = "Fake" if predicted_class_id == 1 else "Genuine"
        
        return {
            "prediction": label,
            "confidence": round(confidence, 4)
        }
