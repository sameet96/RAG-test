"""
Model Manager for handling multiple LLM providers
Supports OpenAI GPT and Llama 3 via Ollama
"""

import os
import logging
import requests
from typing import Optional, Dict, Any
from openai import OpenAI
import ollama

logger = logging.getLogger(__name__)

class ModelManager:
    """Manages different LLM models and providers"""
    
    def __init__(self):
        self.available_models = {
            "OpenAI GPT-3.5-turbo": {
                "provider": "openai",
                "model": "gpt-3.5-turbo",
                "requires_api_key": True,
                "description": "OpenAI's fast and efficient model"
            },
            "OpenAI GPT-4": {
                "provider": "openai", 
                "model": "gpt-4",
                "requires_api_key": True,
                "description": "OpenAI's most capable model"
            },
            "Llama 3": {
                "provider": "ollama",
                "model": "llama3:latest",
                "requires_api_key": False,
                "description": "Meta's Llama 3 model (local)"
            },
            "Llama 2": {
                "provider": "ollama",
                "model": "llama2:latest",
                "requires_api_key": False,
                "description": "Meta's Llama 2 model (local)"
            }
        }
        
        self.current_model = None
        self.current_provider = None
        self.openai_client = None
        self.api_key = None
        
    def get_available_models(self) -> Dict[str, Dict[str, Any]]:
        """Get list of available models"""
        return self.available_models
    
    def check_ollama_connection(self) -> bool:
        """Check if Ollama is running and accessible"""
        try:
            response = requests.get("http://localhost:11434/api/tags", timeout=5)
            return response.status_code == 200
        except Exception as e:
            logger.warning(f"Ollama connection check failed: {e}")
            return False
    
    def get_installed_ollama_models(self) -> list:
        """Get list of installed Ollama models"""
        try:
            if self.check_ollama_connection():
                models = ollama.list()
                return [model.model for model in models.models]
            return []
        except Exception as e:
            logger.warning(f"Failed to get Ollama models: {e}")
            return []
    
    def set_model(self, model_name: str, api_key: Optional[str] = None) -> bool:
        """Set the current model and initialize provider"""
        if model_name not in self.available_models:
            logger.error(f"Model {model_name} not found")
            return False
        
        model_info = self.available_models[model_name]
        self.current_model = model_name
        self.current_provider = model_info["provider"]
        
        # Initialize provider
        if model_info["provider"] == "openai":
            if not api_key:
                logger.error("OpenAI API key required")
                return False
            self.api_key = api_key
            self.openai_client = OpenAI(api_key=api_key)
            logger.info(f"Initialized OpenAI with model: {model_info['model']}")
            
        elif model_info["provider"] == "ollama":
            if not self.check_ollama_connection():
                logger.error("Ollama is not running. Please start Ollama service.")
                return False
            
            # Check if model is installed
            installed_models = self.get_installed_ollama_models()
            if model_info["model"] not in installed_models:
                logger.warning(f"Model {model_info['model']} not installed. Available models: {installed_models}")
                # Try to pull the model
                try:
                    logger.info(f"Pulling model {model_info['model']}...")
                    ollama.pull(model_info["model"])
                    logger.info(f"Successfully pulled {model_info['model']}")
                except Exception as e:
                    logger.error(f"Failed to pull model {model_info['model']}: {e}")
                    return False
            
            logger.info(f"Initialized Ollama with model: {model_info['model']}")
        
        return True
    
    def generate_response(self, prompt: str, context: str = "") -> str:
        """Generate response using the current model"""
        if not self.current_model:
            return "No model selected. Please select a model first."
        
        full_prompt = self._format_prompt(prompt, context)
        
        try:
            if self.current_provider == "openai":
                return self._generate_openai_response(full_prompt)
            elif self.current_provider == "ollama":
                return self._generate_ollama_response(full_prompt)
            else:
                return "Unknown provider"
                
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return f"Error generating response: {str(e)}"
    
    def _format_prompt(self, question: str, context: str) -> str:
        """Format the prompt for the model"""
        if context:
            return f"""Based on the following context, please answer the question. If the answer cannot be found in the context, please say so.

Context:
{context}

Question: {question}

Answer:"""
        else:
            return question
    
    def _generate_openai_response(self, prompt: str) -> str:
        """Generate response using OpenAI"""
        try:
            response = self.openai_client.chat.completions.create(
                model=self.available_models[self.current_model]["model"],
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions based on provided context."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise e
    
    def _generate_ollama_response(self, prompt: str) -> str:
        """Generate response using Ollama"""
        try:
            model_name = self.available_models[self.current_model]["model"]
            response = ollama.generate(
                model=model_name,
                prompt=prompt,
                options={
                    "temperature": 0.7,
                    "num_predict": 1000
                }
            )
            return response['response'].strip()
        except Exception as e:
            logger.error(f"Ollama API error: {e}")
            raise e
    
    def get_model_status(self) -> Dict[str, Any]:
        """Get status of current model and available providers"""
        status = {
            "current_model": self.current_model,
            "current_provider": self.current_provider,
            "openai_available": self.openai_client is not None,
            "ollama_available": self.check_ollama_connection(),
            "ollama_models": self.get_installed_ollama_models()
        }
        return status
    
    def test_model_connection(self) -> Dict[str, Any]:
        """Test connection to current model"""
        if not self.current_model:
            return {"success": False, "message": "No model selected"}
        
        try:
            test_response = self.generate_response("Hello, this is a test message.")
            return {
                "success": True, 
                "message": "Model connection successful",
                "test_response": test_response[:100] + "..." if len(test_response) > 100 else test_response
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Model connection failed: {str(e)}"
            }
