#!/usr/bin/env python3
"""
Test script for the multi-model RAG PDF Chat application
This script demonstrates the model selection and functionality
"""

import sys
import os
sys.path.insert(0, os.path.abspath('..'))

from src.core.model_manager import ModelManager
from src.core.rag_system import RAGSystem

def test_model_manager():
    """Test the ModelManager functionality"""
    print("🧪 Testing Model Manager...")
    
    mm = ModelManager()
    
    # Test available models
    models = mm.get_available_models()
    print(f"✅ Available models: {list(models.keys())}")
    
    # Test model status
    status = mm.get_model_status()
    print(f"✅ Model status: {status}")
    
    # Test OpenAI setup (if API key available)
    if os.getenv('OPENAI_API_KEY'):
        print("\n🤖 Testing OpenAI model...")
        success = mm.set_model("OpenAI GPT-3.5-turbo", os.getenv('OPENAI_API_KEY'))
        if success:
            print("✅ OpenAI model set successfully")
            test_result = mm.test_model_connection()
            print(f"✅ Test result: {test_result['success']}")
            if test_result['success']:
                print(f"   Sample response: {test_result.get('test_response', 'N/A')}")
        else:
            print("❌ Failed to set OpenAI model")
    else:
        print("⚠️ No OpenAI API key found, skipping OpenAI test")
    
    # Test Ollama (if available)
    if status.get('ollama_available', False):
        print("\n🦙 Testing Ollama model...")
        success = mm.set_model("Llama 3")
        if success:
            print("✅ Ollama model set successfully")
            test_result = mm.test_model_connection()
            print(f"✅ Test result: {test_result['success']}")
            if test_result['success']:
                print(f"   Sample response: {test_result.get('test_response', 'N/A')}")
        else:
            print("❌ Failed to set Ollama model")
    else:
        print("⚠️ Ollama not available, skipping Ollama test")

def test_rag_system():
    """Test the RAG system with model manager"""
    print("\n🧪 Testing RAG System...")
    
    rs = RAGSystem()
    
    # Test model methods
    print("✅ Testing RAG system model methods...")
    models = rs.get_available_models()
    print(f"   Available models: {len(models)} models")
    
    status = rs.get_model_status()
    print(f"   Current model: {status.get('current_model', 'None')}")
    
    # Test model setting if OpenAI available
    if os.getenv('OPENAI_API_KEY'):
        success = rs.set_model("OpenAI GPT-3.5-turbo", os.getenv('OPENAI_API_KEY'))
        print(f"   Model setting: {'✅ Success' if success else '❌ Failed'}")

def main():
    """Main test function"""
    print("🚀 Multi-Model RAG PDF Chat - Test Suite")
    print("=" * 50)
    
    try:
        test_model_manager()
        test_rag_system()
        
        print("\n🎉 All tests completed successfully!")
        print("\n📋 Next steps:")
        print("1. Run the application: python run.py")
        print("2. Configure your preferred model in the UI")
        print("3. Upload and process PDF documents")
        print("4. Start chatting with your documents!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
