#!/usr/bin/env python3
"""
Test script to verify LM Studio integration with CAI using the proper OLLAMA_API_BASE approach
"""
import asyncio
import os
import requests
from dotenv import load_dotenv

from cai.agents import get_agent_by_name
from cai.sdk.agents import Runner

# Load environment variables
load_dotenv()

async def test_lmstudio_connection():
    """Test LM Studio connection using CAI's local model approach"""
    
    # Get LM Studio API base
    api_base = os.getenv("LMSTUDIO_API_BASE", "http://localhost:1234/v1")
    models_endpoint = api_base.replace('/v1', '') + '/v1/models'
    
    print(f"Testing connection to LM Studio at: {api_base}")
    
    # Test basic model listing
    try:
        response = requests.get(models_endpoint, timeout=5)
        if response.status_code == 200:
            models_data = response.json()
            models = models_data.get('data', [])
            
            print("Available models in LM Studio:")
            for model in models:
                print(f"  - {model.get('id', 'unknown')}")
            
            if not models:
                print("No models found. Make sure LM Studio is running with a model loaded.")
                return False
        else:
            print(f"HTTP {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error connecting to LM Studio: {e}")
        print("Make sure LM Studio is running and the server is enabled")
        return False
    
    # Test CAI agent with LM Studio
    try:
        model_name = os.getenv("CAI_MODEL", "local-model")
        print(f"\nTesting CAI agent with model: {model_name}")
        
        # Use CAI's built-in agent system
        agent = get_agent_by_name("one_tool_agent")
        
        result = await Runner.run(agent, "Hello! Can you help with cybersecurity tasks? Just respond briefly.")
        print(f"\nAgent response: {result.final_output}")
        return True
        
    except Exception as e:
        print(f"Error testing CAI agent: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_lmstudio_connection())