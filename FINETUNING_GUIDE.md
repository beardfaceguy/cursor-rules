# Fine-Tuning LLM Guide: From Memory Insights to Specialized AI Assistant

## Overview

This guide shows how to fine-tune an existing LLM using insights from your `memory.md` file to create a specialized AI assistant that embodies your architectural patterns, environment gotchas, and development expertise.

## Why Fine-Tune from Memory Insights?

Your `memory.md` contains **goldmine of specialized knowledge**:
- **Architecture Patterns**: Field implementation patterns, GraphQL resolver priorities, UI rendering patterns
- **Environment Gotchas**: Node version requirements, dependency conflicts, service management
- **Critical Commands**: Exact commands for backend startup, database operations, service management
- **Lessons Learned**: Implementation methodologies, common issues and solutions
- **Authentication Info**: Working credentials and access requirements

## Fine-Tuning Approaches

### 1. **LoRA (Low-Rank Adaptation)** - Recommended ⭐
- **Best for**: Most use cases, resource-efficient
- **Pros**: Fast training, small model size, preserves base model knowledge
- **Cons**: Slightly less flexible than full fine-tuning
- **Resource Requirements**: 8-16GB GPU memory

### 2. **QLoRA (Quantized LoRA)** - Most Efficient
- **Best for**: Limited GPU memory
- **Pros**: Can run on consumer GPUs (8GB+), very fast
- **Cons**: May have slight quality trade-offs
- **Resource Requirements**: 6-8GB GPU memory

### 3. **Full Fine-Tuning** - Maximum Performance
- **Best for**: When you have abundant resources
- **Pros**: Maximum adaptation to your domain
- **Cons**: Requires significant computational resources
- **Resource Requirements**: 24GB+ GPU memory

## Data Preparation Process

### Step 1: Extract Training Examples from Memory

Convert your memory insights into instruction-following format:

```json
{
  "instruction": "How should I implement a new field in the Estate model?",
  "context": "I'm working on a GraphQL/Prisma/React stack with PostgreSQL database",
  "response": "Follow the Estate Email Pattern: Add field directly to Estate model with @unique constraint, available for both creation and updates. For auto-generated fields like scanBoxId, generate on backend during estate creation, display-only in frontend. Always check if functionality already exists in backend services before implementing."
}
```

### Step 2: Create Training Dataset Categories

Based on your memory structure, create these training categories:

#### A. Architecture Pattern Questions
```json
{
  "instruction": "What are the different field implementation patterns in this codebase?",
  "response": "There are 4 main patterns: 1) Estate Email Pattern - direct to Estate model with @unique constraint, 2) taxId Pattern - via migration, nullable initially, 3) scanBoxId Pattern - auto-generated backend, display-only frontend, 4) Deceased Fields Pattern - added to Deceased table via migration."
}
```

#### B. Environment Gotcha Questions
```json
{
  "instruction": "How do I start the backend service?",
  "response": "ALWAYS switch to Node 22 first: export NVM_DIR=\"$HOME/.config/nvm\" && [ -s \"$NVM_DIR/nvm.sh\" ] && \\. \"$NVM_DIR/nvm.sh\" && nvm use 22. Then run yarn start in background (NEVER foreground - user loses control). Frontend uses npm run dev (NOT yarn start)."
}
```

#### C. Problem-Solving Questions
```json
{
  "instruction": "I'm getting 'crud resolvers' confusion errors. What's happening?",
  "response": "Generated resolvers are registered FIRST in resolver array, custom resolvers are registered LAST. Frontend mutations may use generated resolvers instead of custom ones. Solution: Add logic to BOTH generated and custom resolvers."
}
```

### Step 3: Generate Training Data Script

Create a script to convert your memory into training examples:

```python
import json
import re
from pathlib import Path

def extract_training_examples(memory_file_path):
    """Extract training examples from memory.md file"""
    
    with open(memory_file_path, 'r') as f:
        content = f.read()
    
    examples = []
    
    # Extract architecture patterns
    patterns_section = extract_section(content, "## Architecture Patterns Discovered")
    if patterns_section:
        examples.extend(create_pattern_examples(patterns_section))
    
    # Extract environment gotchas
    gotchas_section = extract_section(content, "## Environment Gotchas")
    if gotchas_section:
        examples.extend(create_gotcha_examples(gotchas_section))
    
    # Extract critical commands
    commands_section = extract_section(content, "## Critical Commands")
    if commands_section:
        examples.extend(create_command_examples(commands_section))
    
    return examples

def create_pattern_examples(patterns_text):
    """Create training examples from architecture patterns"""
    examples = []
    
    # Field Implementation Patterns
    field_patterns = re.findall(r'- \*\*(.*?)\*\*: (.*?)(?=\n-|\n\n|$)', patterns_text, re.DOTALL)
    
    for pattern_name, description in field_patterns:
        examples.append({
            "instruction": f"What is the {pattern_name} and how should I use it?",
            "context": "I'm implementing new fields in a GraphQL/Prisma/React application",
            "response": f"The {pattern_name}: {description.strip()}"
        })
    
    return examples

def create_gotcha_examples(gotchas_text):
    """Create training examples from environment gotchas"""
    examples = []
    
    # Extract gotcha sections
    sections = re.findall(r'### (.*?)\n(.*?)(?=\n### |$)', gotchas_text, re.DOTALL)
    
    for section_name, content in sections:
        # Extract bullet points
        bullets = re.findall(r'- \*\*(.*?)\*\*: (.*?)(?=\n-|\n\n|$)', content, re.DOTALL)
        
        for gotcha_name, solution in bullets:
            examples.append({
                "instruction": f"I'm having issues with {gotcha_name.lower()}. What should I do?",
                "context": "I'm working on a development environment setup",
                "response": f"For {gotcha_name}: {solution.strip()}"
            })
    
    return examples

def create_command_examples(commands_text):
    """Create training examples from critical commands"""
    examples = []
    
    # Extract code blocks
    code_blocks = re.findall(r'```bash\n(.*?)\n```', commands_text, re.DOTALL)
    
    for i, code_block in enumerate(code_blocks):
        # Extract section headers before code blocks
        section_match = re.search(r'### (.*?)\n```bash', commands_text)
        section_name = section_match.group(1) if section_match else f"Command Set {i+1}"
        
        examples.append({
            "instruction": f"How do I {section_name.lower()}?",
            "context": "I need to execute commands for development environment management",
            "response": f"For {section_name}:\n```bash\n{code_block.strip()}\n```"
        })
    
    return examples

# Usage
memory_file = "cursorRules_v_0_2/.cursor/memory/memory.md"
training_examples = extract_training_examples(memory_file)

# Save as JSONL format
with open("training_data.jsonl", "w") as f:
    for example in training_examples:
        f.write(json.dumps(example) + "\n")

print(f"Generated {len(training_examples)} training examples")
```

## Implementation Guide

### Step 1: Set Up Environment

```bash
# Create virtual environment
python -m venv finetuning_env
source finetuning_env/bin/activate  # On Windows: finetuning_env\Scripts\activate

# Install required packages
pip install torch transformers datasets peft accelerate bitsandbytes
pip install trl  # For instruction tuning
```

### Step 2: Choose Base Model

**Recommended Models:**
- **Llama 2 7B**: Good balance of performance and resource requirements
- **CodeLlama 7B**: Specialized for code, excellent for development tasks
- **Mistral 7B**: Efficient and high-quality
- **Phi-3**: Microsoft's efficient model

### Step 3: LoRA Fine-Tuning Implementation

```python
import torch
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM, 
    TrainingArguments, 
    Trainer
)
from peft import LoraConfig, get_peft_model, TaskType
from datasets import Dataset
import json

class MemoryInsightsTrainer:
    def __init__(self, model_name="microsoft/DialoGPT-medium", base_model=None):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        # Add padding token if not present
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Load model
        if base_model:
            self.model = base_model
        else:
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16,
                device_map="auto"
            )
    
    def load_training_data(self, jsonl_file):
        """Load training data from JSONL file"""
        examples = []
        with open(jsonl_file, 'r') as f:
            for line in f:
                examples.append(json.loads(line))
        
        # Convert to instruction format
        formatted_examples = []
        for example in examples:
            formatted_examples.append({
                "text": f"### Instruction:\n{example['instruction']}\n\n### Context:\n{example.get('context', '')}\n\n### Response:\n{example['response']}"
            })
        
        return Dataset.from_list(formatted_examples)
    
    def setup_lora(self, r=16, lora_alpha=32, lora_dropout=0.1):
        """Setup LoRA configuration"""
        lora_config = LoraConfig(
            task_type=TaskType.CAUSAL_LM,
            r=r,
            lora_alpha=lora_alpha,
            lora_dropout=lora_dropout,
            target_modules=["q_proj", "v_proj", "k_proj", "o_proj"]
        )
        
        self.model = get_peft_model(self.model, lora_config)
        self.model.print_trainable_parameters()
    
    def tokenize_function(self, examples):
        """Tokenize training examples"""
        return self.tokenizer(
            examples["text"],
            truncation=True,
            padding=True,
            max_length=512,
            return_tensors="pt"
        )
    
    def train(self, dataset, output_dir="./memory-insights-model"):
        """Train the model"""
        
        # Tokenize dataset
        tokenized_dataset = dataset.map(
            self.tokenize_function,
            batched=True,
            remove_columns=dataset.column_names
        )
        
        # Training arguments
        training_args = TrainingArguments(
            output_dir=output_dir,
            per_device_train_batch_size=4,
            gradient_accumulation_steps=4,
            num_train_epochs=3,
            learning_rate=2e-4,
            fp16=True,
            logging_steps=10,
            save_steps=100,
            evaluation_strategy="no",
            save_total_limit=2,
        )
        
        # Create trainer
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=tokenized_dataset,
            tokenizer=self.tokenizer,
        )
        
        # Train
        trainer.train()
        
        # Save model
        trainer.save_model()
        self.tokenizer.save_pretrained(output_dir)
        
        return trainer

# Usage
trainer = MemoryInsightsTrainer("microsoft/DialoGPT-medium")
trainer.setup_lora()

# Load your training data
dataset = trainer.load_training_data("training_data.jsonl")

# Train
trainer.train(dataset)
```

### Step 4: QLoRA Implementation (More Efficient)

```python
import torch
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM, 
    BitsAndBytesConfig,
    TrainingArguments, 
    Trainer
)
from peft import LoraConfig, get_peft_model, TaskType
from datasets import Dataset

class QLoRAMemoryTrainer:
    def __init__(self, model_name="microsoft/DialoGPT-medium"):
        self.model_name = model_name
        
        # Quantization config for QLoRA
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16
        )
        
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            quantization_config=bnb_config,
            device_map="auto"
        )
    
    def setup_qlora(self):
        """Setup QLoRA configuration"""
        lora_config = LoraConfig(
            task_type=TaskType.CAUSAL_LM,
            r=16,
            lora_alpha=32,
            lora_dropout=0.1,
            target_modules=["q_proj", "v_proj", "k_proj", "o_proj"],
            bias="none",
        )
        
        self.model = get_peft_model(self.model, lora_config)
        self.model.print_trainable_parameters()
    
    # Rest of the implementation similar to LoRA trainer...
```

## Evaluation Framework

### Step 1: Create Test Cases

```python
def create_evaluation_tests():
    """Create test cases based on your memory insights"""
    
    test_cases = [
        {
            "question": "How should I implement a new auto-generated field in the Estate model?",
            "expected_keywords": ["scanBoxId", "backend generation", "display-only", "frontend"],
            "context": "GraphQL/Prisma/React development"
        },
        {
            "question": "I'm getting dependency conflicts with MUI Lab. What should I do?",
            "expected_keywords": ["legacy-peer-deps", "npm install", "React 19"],
            "context": "Frontend dependency resolution"
        },
        {
            "question": "How do I start the backend service properly?",
            "expected_keywords": ["Node 22", "nvm use", "background", "yarn start"],
            "context": "Backend service management"
        },
        {
            "question": "What's the difference between generated and custom GraphQL resolvers?",
            "expected_keywords": ["generated resolvers", "custom resolvers", "priority", "both"],
            "context": "GraphQL resolver architecture"
        }
    ]
    
    return test_cases

def evaluate_model(model, tokenizer, test_cases):
    """Evaluate the fine-tuned model"""
    
    results = []
    
    for test_case in test_cases:
        # Generate response
        prompt = f"### Instruction:\n{test_case['question']}\n\n### Context:\n{test_case['context']}\n\n### Response:\n"
        
        inputs = tokenizer(prompt, return_tensors="pt")
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=200,
                temperature=0.7,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        response = response.split("### Response:\n")[-1]
        
        # Check for expected keywords
        keyword_matches = sum(1 for keyword in test_case["expected_keywords"] 
                            if keyword.lower() in response.lower())
        
        results.append({
            "question": test_case["question"],
            "response": response,
            "keyword_matches": keyword_matches,
            "total_keywords": len(test_case["expected_keywords"]),
            "score": keyword_matches / len(test_case["expected_keywords"])
        })
    
    return results
```

## Deployment Options

### Option 1: Local Deployment
```python
# Load your fine-tuned model
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

base_model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
model = PeftModel.from_pretrained(base_model, "./memory-insights-model")
tokenizer = AutoTokenizer.from_pretrained("./memory-insights-model")

# Use for inference
def ask_memory_assistant(question, context=""):
    prompt = f"### Instruction:\n{question}\n\n### Context:\n{context}\n\n### Response:\n"
    inputs = tokenizer(prompt, return_tensors="pt")
    
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=200, temperature=0.7)
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response.split("### Response:\n")[-1]
```

### Option 2: API Deployment
```python
from flask import Flask, request, jsonify
import torch

app = Flask(__name__)

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.json
    question = data.get('question', '')
    context = data.get('context', '')
    
    response = ask_memory_assistant(question, context)
    
    return jsonify({
        'question': question,
        'response': response,
        'context': context
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

## Expected Results

After fine-tuning, your model should be able to:

✅ **Answer architecture questions** with specific patterns from your codebase
✅ **Provide exact commands** for environment setup and service management  
✅ **Explain gotchas** with precise solutions from your experience
✅ **Guide implementation** following your established patterns
✅ **Troubleshoot issues** using your lessons learned

## Cost Estimation

- **LoRA Training**: $5-20 (depending on model size and training time)
- **QLoRA Training**: $2-10 (more efficient)
- **Full Fine-tuning**: $50-200 (resource intensive)
- **Inference**: $0.001-0.01 per request (depending on deployment)

## Next Steps

1. **Extract your training data** using the provided script
2. **Choose your approach** (LoRA recommended for most cases)
3. **Set up training environment** with required packages
4. **Train your model** using the provided code
5. **Evaluate performance** with test cases
6. **Deploy for use** in your development workflow

---

**Result**: You'll have a specialized AI assistant that knows your codebase patterns, environment quirks, and development expertise - essentially your `memory.md` file as an intelligent, interactive assistant!
