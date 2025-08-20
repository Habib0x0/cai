# LM Studio Integration with CAI

This guide explains how to integrate LM Studio with the CAI (Cybersecurity AI) framework for local model inference.

## Overview

LM Studio is a desktop application that allows you to run large language models locally on your machine. CAI now has native support for LM Studio alongside Ollama, providing you with flexible options for local model deployment.

## Prerequisites

1. **LM Studio**: Download and install from [https://lmstudio.ai/](https://lmstudio.ai/)
2. **CAI Framework**: Install with `pip install cai-framework`
3. **A compatible model**: Download a model in LM Studio (e.g., Llama, Qwen, Mistral)

## Setup Instructions

### 1. Configure LM Studio

1. **Download a Model**: In LM Studio, browse and download a model suitable for cybersecurity tasks
2. **Load the Model**: Click on the model to load it into memory
3. **Start the Server**: 
   - Go to the "Local Server" tab
   - Click "Start Server"
   - Note the server URL (typically `http://localhost:1234`)

### 2. Configure CAI

Create or update your `.env` file:

```bash
# LM Studio Configuration
LMSTUDIO_API_BASE="http://localhost:1234/v1"
CAI_MODEL="your-exact-model-name"

# Required placeholder (not used with local models)
OPENAI_API_KEY="sk-1234"

# Optional settings
CAI_TRACING="false"
CAI_TELEMETRY="false"
CAI_STREAM="false"
PROMPT_TOOLKIT_NO_CPR=1
```

### 3. Find Your Model Name

To get the exact model name, you can:

**Option A: Check via API**
```bash
curl http://localhost:1234/v1/models
```

**Option B: Use CAI's model command**
```bash
cai
/model-show
```

**Option C: Check LM Studio interface**
The model name is usually displayed in the LM Studio interface when the model is loaded.

## Usage Examples

### Basic CLI Usage

```bash
# Start CAI with LM Studio
cai

# Use specific agent
CAI_AGENT_TYPE="one_tool_agent" cai

# Override model temporarily
CAI_MODEL="llama-3.2-3b-instruct" cai
```

### Python SDK Usage

```python
import asyncio
from cai.agents import get_agent_by_name
from cai.sdk.agents import Runner

async def main():
    # Get a cybersecurity agent (automatically uses LM Studio config)
    agent = get_agent_by_name("one_tool_agent")
    
    # Run a cybersecurity task
    result = await Runner.run(
        agent, 
        "Analyze this system for potential vulnerabilities"
    )
    print(result.final_output)

asyncio.run(main())
```

### Advanced Configuration

You can configure different models for different agents:

```bash
# In .env file
LMSTUDIO_API_BASE="http://localhost:1234/v1"
CAI_MODEL="llama-3.2-3b-instruct"

# Agent-specific model overrides
CAI_ONE_TOOL_AGENT_MODEL="qwen2.5-14b-instruct"
CAI_RED_TEAMER_MODEL="llama-3.2-3b-instruct"
```

## Features Supported

### ✅ Supported Features
- All CAI agent types
- Tool execution and function calling
- Streaming responses (set `CAI_STREAM=true`)
- Cost tracking (shows $0.00 for local models)
- Model switching via `/model` command
- Parallel agent execution
- Memory and context management

### ⚠️ Limitations
- Model performance depends on your hardware
- Some models may not support function calling
- Response times vary based on model size and hardware

## Troubleshooting

### Common Issues

**1. Connection Refused**
```
Error: Cannot connect to LM Studio
```
- Ensure LM Studio is running
- Check that the server is started in LM Studio
- Verify the port (default: 1234)

**2. Model Not Found**
```
Error: Model 'model-name' not found
```
- Check the exact model name with `/model-show`
- Ensure the model is loaded in LM Studio
- Verify `CAI_MODEL` in your `.env` file

**3. Slow Responses**
- Try a smaller model
- Increase your system RAM
- Close other applications to free up resources

### Performance Tips

1. **Choose the Right Model Size**:
   - 3B parameters: Fast, good for basic tasks
   - 7B parameters: Balanced performance
   - 14B+ parameters: Better quality, slower

2. **Hardware Optimization**:
   - Use GPU acceleration if available
   - Ensure sufficient RAM (8GB+ recommended)
   - Use SSD storage for faster model loading

3. **CAI Configuration**:
   - Set `CAI_STREAM=true` for real-time responses
   - Use `CAI_TRACING=false` to reduce overhead
   - Adjust `CAI_MAX_TURNS` to limit conversation length

## Integration with Other Tools

### Using with Ollama (Fallback)

You can configure both LM Studio and Ollama:

```bash
# Primary: LM Studio
LMSTUDIO_API_BASE="http://localhost:1234/v1"

# Fallback: Ollama
OLLAMA_API_BASE="http://localhost:11434/v1"

# CAI will auto-detect which is available
```

### Docker Deployment

For containerized deployments, you can expose LM Studio:

```bash
# Run LM Studio with network access
# Then configure CAI container
LMSTUDIO_API_BASE="http://host.docker.internal:1234/v1"
```

## Example Workflows

### 1. Bug Bounty Hunting
```bash
CAI_AGENT_TYPE="bug_bounter" CAI_MODEL="qwen2.5-14b" cai
```

### 2. Red Team Operations
```bash
CAI_AGENT_TYPE="red_teamer" CAI_MODEL="llama-3.2-7b" cai
```

### 3. Network Analysis
```bash
CAI_AGENT_TYPE="network_traffic_analyzer" CAI_MODEL="mistral-7b" cai
```

## Best Practices

1. **Model Selection**: Choose models with good instruction-following capabilities
2. **Resource Management**: Monitor system resources during operation
3. **Security**: Keep LM Studio server local (don't expose to internet)
4. **Updates**: Keep both LM Studio and CAI updated
5. **Testing**: Use the provided test script to verify integration

## Support

For issues specific to:
- **LM Studio**: Check [LM Studio documentation](https://lmstudio.ai/docs)
- **CAI Integration**: Open an issue on the [CAI GitHub repository](https://github.com/aliasrobotics/cai)
- **Model Performance**: Consider trying different models or adjusting hardware

## Example Test Script

Run the integration test:

```bash
python examples/cai/lmstudio_integration.py
```

This will verify your LM Studio connection and test basic CAI functionality.