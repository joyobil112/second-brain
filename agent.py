import ollama
from pydantic import BaseModel
from typing import Literal
import json

# 1. Define the exact structure we demand from the LLM
class DocumentClassification(BaseModel):
    # The LLM MUST choose one of these exact strings
    category: Literal['Theology', 'Machine Learning', 'Business', 'Discipline', 'Uncategorized']
    confidence_score: float # Forces the LLM to evaluate its own decision (0.0 to 1.0)
    reasoning: str # Asking for reasoning first improves the LLM's accuracy

class TextClassifier:
    def __init__(self, model_name: str = "llama3.2"):
        """
        Initializes the classifier. 
        Make sure you have pulled this model via your terminal first (e.g., `ollama run llama3.2`)
        """
        self.model_name = model_name

    def categorize_text(self, text: str) -> dict:
        """Sends the text to the local LLM and returns a structured JSON classification."""
        
        # We truncate the text slightly to avoid blowing up the context window on massive PDFs
        truncated_text = text[:4000] 
        
        prompt = f"""
        You are an intelligent classification routing agent for a Personal Knowledge Management system.
        Read the following text and categorize it into exactly one of the allowed categories.
        
        Text to classify:
        ---
        {truncated_text}
        ---
        """

        try:
            # 2. Call Ollama, passing the Pydantic schema to enforce JSON output
            response = ollama.chat(
                model=self.model_name,
                messages=[{'role': 'user', 'content': prompt}],
                format=DocumentClassification.model_json_schema(),
                options={'temperature': 0.1} # Low temperature for highly deterministic routing
            )
            
            # 3. Parse the string response back into a valid Python dictionary using Pydantic
            raw_json = response['message']['content']
            validated_data = DocumentClassification.model_validate_json(raw_json)
            
            return validated_data.model_dump()
            
        except Exception as e:
            print(f"❌ LLM Classification Failed: {e}")
            # Fallback to prevent the pipeline from crashing
            return {
                "category": "Uncategorized", 
                "confidence_score": 0.0, 
                "reasoning": f"Error during classification: {str(e)}"
            }