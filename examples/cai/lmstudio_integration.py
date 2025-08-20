#!/usr/bin/env python3
"""
LM Studio Integration Example for CAI Framework

This example demonstrates how to use CAI with LM Studio local models.
"""
import asyncio
import os
from dotenv import load_dotenv

from cai.agents import get_agent_by_name
from cai.sdk.agents import Runner
from cai.util import get_lmstudio_api_base

# Load environment variables
load_dotenv()

async def main():
    """Main example function demonstrating LM Studio integration."""
    
    print("🤖 CAI + LM Studio Integration Example")
    print("=" * 50)
    
    # Check LM Studio configuration
    lmstudio_base = get_lmstudio_api_base()
    model_name = os.getenv("CAI_MODEL", "local-model")
    
    print(f"LM Studio API Base: {lmstudio_base}")
    print(f"Model Name: {model_name}")
    print()
    
    # Test connection to LM Studio
    try:
        import requests
        response = requests.get(f"{lmstudio_base}/models", timeout=5)
        if response.status_code == 200:
            models_data = response.json()
            models = models_data.get('data', [])
            print(f"✅ Connected to LM Studio - {len(models)} models available")
            for model in models[:3]:  # Show first 3 models
                print(f"   - {model.get('id', 'unknown')}")
            if len(models) > 3:
                print(f"   ... and {len(models) - 3} more")
        else:
            print(f"❌ LM Studio connection failed: HTTP {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Cannot connect to LM Studio: {e}")
        print("Make sure LM Studio is running with the server enabled")
        return
    
    print("\n" + "=" * 50)
    print("🔧 Testing CAI Agent with LM Studio")
    print("=" * 50)
    
    try:
        # Get a cybersecurity agent
        agent = get_agent_by_name("one_tool_agent")
        
        # Test basic interaction
        print("\n🧪 Test 1: Basic cybersecurity question")
        result = await Runner.run(
            agent, 
            "What are the top 3 most common web application vulnerabilities? Be concise."
        )
        print(f"Agent Response: {result.final_output}")
        
        # Test with tool usage
        print("\n🧪 Test 2: System command execution")
        result = await Runner.run(
            agent,
            "Check what operating system we're running on using a system command."
        )
        print(f"Agent Response: {result.final_output}")
        
        print("\n✅ LM Studio integration successful!")
        
    except Exception as e:
        print(f"❌ Error running CAI agent: {e}")
        return

if __name__ == "__main__":
    # Check environment setup
    if not os.getenv("LMSTUDIO_API_BASE") and not os.getenv("OLLAMA_API_BASE"):
        print("⚠️  Warning: No LMSTUDIO_API_BASE configured in .env file")
        print("   Add: LMSTUDIO_API_BASE='http://localhost:1234/v1'")
        print("   And: CAI_MODEL='your-model-name'")
        print()
    
    asyncio.run(main())