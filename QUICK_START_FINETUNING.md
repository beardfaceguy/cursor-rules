# Quick Start: Fine-Tuning LLM from Memory Insights

## 🚀 Get Started in 5 Steps

### Step 1: Extract Training Data
```bash
# Extract training examples from your memory.md
python extract_training_data.py cursorRules_v_0_2/.cursor/memory/memory.md -o training_data.jsonl

# This creates ~50-100 training examples from your insights
```

### Step 2: Set Up Environment
```bash
# Create virtual environment
python -m venv finetuning_env
source finetuning_env/bin/activate  # On Windows: finetuning_env\Scripts\activate

# Install required packages
pip install torch transformers datasets peft accelerate bitsandbytes trl
```

### Step 3: Choose Your Approach

#### Option A: LoRA (Recommended) - 8-16GB GPU
```python
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import LoraConfig, get_peft_model, TaskType

# Load model
model_name = "microsoft/DialoGPT-medium"  # or "mistralai/Mistral-7B-v0.1"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Setup LoRA
lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    r=16,
    lora_alpha=32,
    lora_dropout=0.1,
    target_modules=["q_proj", "v_proj", "k_proj", "o_proj"]
)
model = get_peft_model(model, lora_config)
```

#### Option B: QLoRA (Most Efficient) - 6-8GB GPU
```python
from transformers import BitsAndBytesConfig

# Quantization config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

# Load quantized model
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map="auto"
)
```

### Step 4: Train Your Model
```python
from transformers import TrainingArguments, Trainer
from datasets import Dataset
import json

# Load training data
examples = []
with open("training_data.jsonl", "r") as f:
    for line in f:
        examples.append(json.loads(line))

# Format for training
formatted_examples = []
for example in examples:
    formatted_examples.append({
        "text": f"### Instruction:\n{example['instruction']}\n\n### Context:\n{example.get('context', '')}\n\n### Response:\n{example['response']}"
    })

dataset = Dataset.from_list(formatted_examples)

# Tokenize
def tokenize_function(examples):
    return tokenizer(examples["text"], truncation=True, padding=True, max_length=512)

tokenized_dataset = dataset.map(tokenize_function, batched=True, remove_columns=dataset.column_names)

# Training arguments
training_args = TrainingArguments(
    output_dir="./memory-insights-model",
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    num_train_epochs=3,
    learning_rate=2e-4,
    fp16=True,
    logging_steps=10,
    save_steps=100,
)

# Train
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    tokenizer=tokenizer,
)

trainer.train()
trainer.save_model()
```

### Step 5: Evaluate Your Model
```bash
# Evaluate the fine-tuned model
python evaluate_model.py microsoft/DialoGPT-medium ./memory-insights-model -o evaluation_results.json
```

## 🎯 Expected Results

After training, your model should be able to:

✅ **Answer architecture questions**: "How should I implement a new field?" → Specific patterns from your codebase
✅ **Provide exact commands**: "How do I start the backend?" → Exact Node 22 + yarn start commands  
✅ **Explain gotchas**: "MUI Lab conflicts?" → npm install --legacy-peer-deps solution
✅ **Guide implementation**: Following your established patterns and methodologies

## 📊 Sample Training Data

Your extracted training data will look like this:

```json
{
  "instruction": "How should I implement a new auto-generated field in the Estate model?",
  "context": "I'm working on a GraphQL/Prisma/React application with PostgreSQL database",
  "response": "Follow the scanBoxId Pattern: Auto-generated on backend during estate creation, display-only in frontend. Generate on backend during estate creation, include in estate creation data, display in UI with fallback when empty."
}
```

## 💰 Cost Estimates

- **Training**: $5-20 (LoRA) / $2-10 (QLoRA)
- **Inference**: $0.001-0.01 per request
- **Total**: Under $25 for complete setup

## 🔧 Troubleshooting

### Common Issues:
1. **CUDA out of memory**: Use QLoRA or smaller batch size
2. **Poor responses**: Increase training epochs or learning rate
3. **Overfitting**: Reduce LoRA rank or add dropout

### Quick Fixes:
```python
# Reduce memory usage
training_args.per_device_train_batch_size = 2
training_args.gradient_accumulation_steps = 8

# Improve quality
training_args.num_train_epochs = 5
training_args.learning_rate = 1e-4
```

## 🚀 Next Steps

1. **Deploy locally**: Use the model for your development workflow
2. **Create API**: Build a simple Flask/FastAPI wrapper
3. **Integrate with IDE**: Connect to your development environment
4. **Share knowledge**: Deploy for your team to use

---

**Result**: You'll have a specialized AI assistant that knows your codebase patterns, environment quirks, and development expertise - essentially your `memory.md` file as an intelligent, interactive assistant!
