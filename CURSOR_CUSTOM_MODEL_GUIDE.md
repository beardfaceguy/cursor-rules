# Cursor Custom Model Integration Guide

## Overview

This guide shows how to integrate your fine-tuned model directly into Cursor Agent, allowing you to use your specialized development knowledge within Cursor's interface.

## ⚠️ Important Limitations

**Agent Mode Limitation**: As of 2025, custom models accessed via API do **NOT** support Agent mode in Cursor. This means:
- ✅ **Chat Mode**: Works with custom models
- ✅ **Code Generation**: Works with custom models  
- ❌ **Agent Mode**: Autonomous code editing, tool usage, file operations - **NOT AVAILABLE**

**Workaround**: Use Agent mode with default models, then switch to custom model for specific tasks.

## Integration Methods

### Method 1: Local Model with LiteLLM Proxy (Recommended)

#### Step 1: Set Up Local Model Server
```bash
# Install LiteLLM
pip install litellm

# Create local server configuration
cat > local_model_server.py << 'EOF'
from litellm import completion
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/v1/chat/completions")
async def chat_completions(request: dict):
    """Proxy requests to your fine-tuned model"""
    
    # Load your fine-tuned model
    from transformers import AutoTokenizer, AutoModelForCausalLM
    from peft import PeftModel
    
    # Initialize model (do this once, cache it)
    if not hasattr(app, 'model'):
        base_model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
        app.model = PeftModel.from_pretrained(base_model, "./memory-insights-model")
        app.tokenizer = AutoTokenizer.from_pretrained("./memory-insights-model")
    
    # Generate response
    messages = request.get("messages", [])
    prompt = "\n".join([msg["content"] for msg in messages])
    
    inputs = app.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
    
    with torch.no_grad():
        outputs = app.model.generate(
            **inputs,
            max_new_tokens=200,
            temperature=0.7,
            do_sample=True,
            pad_token_id=app.tokenizer.eos_token_id
        )
    
    response = app.tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return {
        "choices": [{
            "message": {
                "content": response,
                "role": "assistant"
            }
        }]
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
EOF

# Run the server
python local_model_server.py
```

#### Step 2: Expose Local Server (Required for Cursor)
```bash
# Install ngrok
npm install -g ngrok

# Expose your local server
ngrok http 8000

# Note the ngrok URL (e.g., https://abc123.ngrok.io)
```

#### Step 3: Configure Cursor
1. **Open Cursor Settings** → `AI Models`
2. **Add Custom Model**:
   ```json
   {
     "models": {
       "memory-insights": {
         "name": "Memory Insights Assistant",
         "apiKey": "dummy-key",
         "baseUrl": "https://abc123.ngrok.io/v1",
         "model": "memory-insights",
         "contextLength": 4096,
         "temperature": 0.7
       }
     }
   }
   ```
3. **Save Settings**

### Method 2: OpenAI-Compatible API Endpoint

#### Step 1: Deploy Your Model
```python
# Deploy to cloud service (AWS, GCP, Azure, etc.)
# Or use services like:
# - Replicate
# - Hugging Face Inference API
# - AWS SageMaker
# - Google Cloud AI Platform

# Example deployment script
import boto3
from sagemaker.huggingface import HuggingFaceModel

# Deploy to SageMaker
huggingface_model = HuggingFaceModel(
    model_data="s3://your-bucket/memory-insights-model.tar.gz",
    role="arn:aws:iam::123456789012:role/SageMakerRole",
    transformers_version="4.26",
    pytorch_version="1.13",
    py_version="py39"
)

predictor = huggingface_model.deploy(
    initial_instance_count=1,
    instance_type="ml.m5.large"
)
```

#### Step 2: Configure Cursor
```json
{
  "models": {
    "memory-insights-cloud": {
      "name": "Memory Insights (Cloud)",
      "apiKey": "your-cloud-api-key",
      "baseUrl": "https://your-deployed-endpoint.com/v1",
      "model": "memory-insights",
      "contextLength": 4096
    }
  }
}
```

### Method 3: Custom Agent Definition

#### Step 1: Create Agent Configuration
```bash
# Create agent directory
mkdir -p .cursor/agents

# Create agent definition
cat > .cursor/agents/memory-insights-agent.mdc << 'EOF'
---
name: 'Memory Insights Assistant'
model: memory-insights
description: 'Specialized assistant with deep knowledge of our codebase patterns, environment gotchas, and development expertise.'
type: 'Development Expert, Architecture Guide'
icon: 'brain-circuit'
actions:
  auto_apply_edits: false  # Agent mode not supported
  auto_run: false
  auto_fix_errors: false
tools:
  all: false
  search:
    codebase: true
    web: true
    grep: true
    list_directory: true
    search_files: true
    read_file: true
    fetch_rules: true
  edit:
    edit_and_reapply: false  # Agent mode limitation
    delete_file: false
  run:
    terminal: false
integrations:
  mcp_get_some_data: true
---

# Memory Insights Assistant

I am a specialized AI assistant trained on your development team's accumulated knowledge, including:

## Architecture Patterns
- Field implementation patterns (Estate Email, taxId, scanBoxId)
- GraphQL resolver priorities and best practices
- UI conditional rendering patterns
- Database migration strategies

## Environment Gotchas
- Backend startup procedures (Node 22, nvm, background processes)
- Dependency resolution (legacy-peer-deps for MUI Lab conflicts)
- Service management and cleanup
- Database user permissions and setup

## Critical Commands
- Backend startup: `export NVM_DIR="$HOME/.config/nvm" && [ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" && nvm use 22`
- Frontend startup: `npm install --legacy-peer-deps && npm run dev`
- Database operations: `npx prisma migrate status`, `npx prisma migrate deploy`
- Service cleanup: `pkill -f "ts-node-dev" && pkill -f "yarn start"`

## Lessons Learned
- Jira-First Analysis methodology
- Complete Field Analysis before implementation
- Backend-First Verification approach
- Complete Data Flow Tracing (Database → Backend → GraphQL → Frontend)

## Authentication Information
- Working credentials: `admintest@meetalix.com` / `te8mAlix!`
- Access requirements: AWS Cognito authentication, Admin/SuperAdmin roles
- Site URL: http://localhost:3000/

I can help you with implementation patterns, environment setup, troubleshooting, and providing exact commands for your development workflow.
EOF
```

## Usage Strategies

### Strategy 1: Hybrid Approach (Recommended)
1. **Use Default Models** for Agent mode (autonomous operations)
2. **Switch to Custom Model** for specific knowledge-intensive tasks:
   - Architecture pattern questions
   - Environment troubleshooting
   - Command generation
   - Implementation guidance

### Strategy 2: Specialized Workflows
1. **Chat Mode**: Use custom model for Q&A about your codebase
2. **Code Generation**: Use custom model for pattern-specific code
3. **Agent Mode**: Use default models for autonomous operations

### Strategy 3: Context Switching
```bash
# Quick model switching in Cursor
# Ctrl+Shift+P → "AI: Switch Model" → Select your custom model
```

## Testing Your Integration

### Test Cases for Custom Model
```python
# Test your custom model integration
test_questions = [
    "How should I implement a new auto-generated field in the Estate model?",
    "I'm getting MUI Lab dependency conflicts. What should I do?",
    "How do I start the backend service properly?",
    "What are the working authentication credentials?",
    "How do GraphQL resolvers work in this codebase?"
]

# Expected responses should include your specific patterns and commands
```

## Performance Optimization

### Model Optimization
```python
# Optimize your model for Cursor integration
def optimize_for_cursor(model, tokenizer):
    """Optimize model for Cursor's usage patterns"""
    
    # Reduce model size for faster inference
    model.half()  # Use FP16
    
    # Enable caching for repeated requests
    model.config.use_cache = True
    
    # Optimize generation parameters
    generation_config = {
        "max_new_tokens": 150,  # Shorter responses for Cursor
        "temperature": 0.7,
        "do_sample": True,
        "top_p": 0.9,
        "repetition_penalty": 1.1
    }
    
    return model, generation_config
```

### Server Optimization
```python
# Optimize your local server
import asyncio
from concurrent.futures import ThreadPoolExecutor

class OptimizedModelServer:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.model_cache = {}
    
    async def generate_response(self, prompt):
        """Async response generation"""
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            self.executor, 
            self._generate_sync, 
            prompt
        )
        return response
```

## Troubleshooting

### Common Issues
1. **Model Not Loading**: Check file paths and model format
2. **Slow Responses**: Optimize model size and enable caching
3. **Connection Errors**: Verify ngrok tunnel and server status
4. **Agent Mode Not Working**: Expected limitation - use hybrid approach

### Debug Commands
```bash
# Check server status
curl -X POST http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "test"}]}'

# Check ngrok tunnel
ngrok status

# Monitor server logs
tail -f local_model_server.log
```

## Expected Results

After integration, you'll have:

✅ **Specialized Knowledge**: Your custom model knows your specific patterns
✅ **Exact Commands**: Provides precise commands for your environment
✅ **Architecture Guidance**: Understands your codebase patterns
✅ **Troubleshooting**: Knows your common issues and solutions
✅ **Seamless Integration**: Works within Cursor's interface

## Limitations and Workarounds

### Current Limitations
- ❌ **Agent Mode**: Not supported with custom models
- ❌ **Tool Usage**: Limited with custom models
- ❌ **Autonomous Operations**: Requires default models

### Workarounds
- ✅ **Hybrid Approach**: Use both model types strategically
- ✅ **Context Switching**: Quick model switching in Cursor
- ✅ **Specialized Agents**: Custom agent definitions for specific tasks
- ✅ **Workflow Integration**: Incorporate custom model into development workflow

---

**Result**: You'll have your specialized development knowledge integrated directly into Cursor, providing expert guidance while working within Cursor's interface!
