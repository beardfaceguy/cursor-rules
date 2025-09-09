#!/usr/bin/env python3
"""
Memory Insights Model Evaluator

This script evaluates the performance of your fine-tuned model
by testing it against questions derived from your memory insights.
"""

import json
import torch
import argparse
from pathlib import Path
from typing import List, Dict, Any, Tuple
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

class MemoryInsightsEvaluator:
    def __init__(self, base_model_name: str, fine_tuned_model_path: str):
        self.base_model_name = base_model_name
        self.fine_tuned_model_path = fine_tuned_model_path
        
        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(fine_tuned_model_path)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Load base model
        self.base_model = AutoModelForCausalLM.from_pretrained(base_model_name)
        
        # Load fine-tuned model
        self.fine_tuned_model = PeftModel.from_pretrained(self.base_model, fine_tuned_model_path)
        self.fine_tuned_model.eval()
    
    def create_evaluation_tests(self) -> List[Dict[str, Any]]:
        """Create comprehensive test cases based on memory insights"""
        
        test_cases = [
            # Architecture Pattern Tests
            {
                "category": "Architecture Patterns",
                "question": "How should I implement a new auto-generated field in the Estate model?",
                "expected_keywords": ["scanBoxId", "backend generation", "display-only", "frontend", "auto-generated"],
                "context": "I'm implementing new fields in a GraphQL/Prisma/React application",
                "difficulty": "medium"
            },
            {
                "category": "Architecture Patterns", 
                "question": "What's the difference between Estate Email Pattern and taxId Pattern?",
                "expected_keywords": ["Estate Email", "taxId", "unique constraint", "migration", "nullable"],
                "context": "I need to understand field implementation patterns",
                "difficulty": "medium"
            },
            {
                "category": "Architecture Patterns",
                "question": "How do GraphQL resolvers work in this codebase?",
                "expected_keywords": ["generated resolvers", "custom resolvers", "priority", "registered", "both"],
                "context": "I'm implementing GraphQL resolvers",
                "difficulty": "hard"
            },
            
            # Environment Gotcha Tests
            {
                "category": "Environment Gotchas",
                "question": "I'm getting dependency conflicts with MUI Lab. What should I do?",
                "expected_keywords": ["legacy-peer-deps", "npm install", "React 19", "MUI Lab"],
                "context": "Frontend dependency resolution issues",
                "difficulty": "easy"
            },
            {
                "category": "Environment Gotchas",
                "question": "How do I start the backend service properly?",
                "expected_keywords": ["Node 22", "nvm use", "background", "yarn start", "foreground"],
                "context": "Backend service management",
                "difficulty": "medium"
            },
            {
                "category": "Environment Gotchas",
                "question": "I'm having database permission issues with Prisma migrations. What's wrong?",
                "expected_keywords": ["patrickclawson", "CREATEDB", "permissions", "superuser", "shadow database"],
                "context": "Database migration problems",
                "difficulty": "hard"
            },
            
            # Critical Commands Tests
            {
                "category": "Critical Commands",
                "question": "How do I check migration status and apply pending migrations?",
                "expected_keywords": ["prisma migrate status", "prisma migrate deploy", "npx"],
                "context": "Database migration management",
                "difficulty": "easy"
            },
            {
                "category": "Critical Commands",
                "question": "How do I kill all backend processes and clean up services?",
                "expected_keywords": ["pkill", "ts-node-dev", "yarn start", "ps aux"],
                "context": "Service cleanup and management",
                "difficulty": "medium"
            },
            
            # Lessons Learned Tests
            {
                "category": "Lessons Learned",
                "question": "What's the proper methodology for implementing new fields?",
                "expected_keywords": ["Jira-First", "Complete Field Analysis", "Backend-First", "Data Flow Tracing"],
                "context": "Implementation methodology",
                "difficulty": "hard"
            },
            {
                "category": "Lessons Learned",
                "question": "I'm confused about 'crud resolvers'. What's happening?",
                "expected_keywords": ["generated resolvers", "custom resolvers", "precedence", "both"],
                "context": "GraphQL resolver confusion",
                "difficulty": "medium"
            },
            
            # Authentication Tests
            {
                "category": "Authentication",
                "question": "What are the working authentication credentials for testing?",
                "expected_keywords": ["admintest@meetalix.com", "te8mAlix!", "Admin", "localhost:3000"],
                "context": "Application testing access",
                "difficulty": "easy"
            },
            {
                "category": "Authentication",
                "question": "What are the access requirements for this application?",
                "expected_keywords": ["AWS Cognito", "Admin", "SuperAdmin", "authentication required"],
                "context": "Application access setup",
                "difficulty": "medium"
            }
        ]
        
        return test_cases
    
    def generate_response(self, question: str, context: str = "", model_type: str = "fine_tuned") -> str:
        """Generate response from the model"""
        
        model = self.fine_tuned_model if model_type == "fine_tuned" else self.base_model
        
        prompt = f"### Instruction:\n{question}\n\n### Context:\n{context}\n\n### Response:\n"
        
        inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=200,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
                eos_token_id=self.tokenizer.eos_token_id
            )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract just the response part
        if "### Response:\n" in response:
            response = response.split("### Response:\n")[-1]
        
        return response.strip()
    
    def evaluate_keywords(self, response: str, expected_keywords: List[str]) -> Tuple[int, float, List[str]]:
        """Evaluate keyword matches in response"""
        response_lower = response.lower()
        matched_keywords = []
        
        for keyword in expected_keywords:
            if keyword.lower() in response_lower:
                matched_keywords.append(keyword)
        
        matches = len(matched_keywords)
        score = matches / len(expected_keywords) if expected_keywords else 0
        
        return matches, score, matched_keywords
    
    def evaluate_test_case(self, test_case: Dict[str, Any], model_type: str = "fine_tuned") -> Dict[str, Any]:
        """Evaluate a single test case"""
        
        response = self.generate_response(
            test_case["question"], 
            test_case["context"], 
            model_type
        )
        
        matches, score, matched_keywords = self.evaluate_keywords(
            response, 
            test_case["expected_keywords"]
        )
        
        return {
            "category": test_case["category"],
            "question": test_case["question"],
            "response": response,
            "expected_keywords": test_case["expected_keywords"],
            "matched_keywords": matched_keywords,
            "matches": matches,
            "total_keywords": len(test_case["expected_keywords"]),
            "score": score,
            "difficulty": test_case["difficulty"],
            "model_type": model_type
        }
    
    def run_evaluation(self, test_cases: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Run comprehensive evaluation"""
        
        if test_cases is None:
            test_cases = self.create_evaluation_tests()
        
        results = {
            "fine_tuned": [],
            "base_model": [],
            "summary": {}
        }
        
        print("Running evaluation on fine-tuned model...")
        for test_case in test_cases:
            result = self.evaluate_test_case(test_case, "fine_tuned")
            results["fine_tuned"].append(result)
        
        print("Running evaluation on base model for comparison...")
        for test_case in test_cases:
            result = self.evaluate_test_case(test_case, "base_model")
            results["base_model"].append(result)
        
        # Calculate summary statistics
        results["summary"] = self._calculate_summary(results)
        
        return results
    
    def _calculate_summary(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate summary statistics"""
        
        summary = {
            "fine_tuned": {},
            "base_model": {},
            "improvement": {}
        }
        
        for model_type in ["fine_tuned", "base_model"]:
            scores = [r["score"] for r in results[model_type]]
            matches = [r["matches"] for r in results[model_type]]
            
            summary[model_type] = {
                "average_score": sum(scores) / len(scores),
                "total_matches": sum(matches),
                "perfect_scores": sum(1 for s in scores if s == 1.0),
                "zero_scores": sum(1 for s in scores if s == 0.0),
                "category_scores": self._calculate_category_scores(results[model_type])
            }
        
        # Calculate improvement
        ft_avg = summary["fine_tuned"]["average_score"]
        bm_avg = summary["base_model"]["average_score"]
        
        summary["improvement"] = {
            "score_improvement": ft_avg - bm_avg,
            "percentage_improvement": ((ft_avg - bm_avg) / bm_avg * 100) if bm_avg > 0 else 0,
            "better_performance": ft_avg > bm_avg
        }
        
        return summary
    
    def _calculate_category_scores(self, results: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate average scores by category"""
        category_scores = {}
        
        for result in results:
            category = result["category"]
            if category not in category_scores:
                category_scores[category] = []
            category_scores[category].append(result["score"])
        
        # Calculate averages
        for category in category_scores:
            category_scores[category] = sum(category_scores[category]) / len(category_scores[category])
        
        return category_scores
    
    def print_evaluation_report(self, results: Dict[str, Any]):
        """Print detailed evaluation report"""
        
        print("\n" + "="*80)
        print("MEMORY INSIGHTS MODEL EVALUATION REPORT")
        print("="*80)
        
        # Summary statistics
        summary = results["summary"]
        
        print(f"\n📊 OVERALL PERFORMANCE:")
        print(f"   Fine-tuned Model Average Score: {summary['fine_tuned']['average_score']:.3f}")
        print(f"   Base Model Average Score:       {summary['base_model']['average_score']:.3f}")
        print(f"   Improvement:                    {summary['improvement']['score_improvement']:+.3f}")
        print(f"   Percentage Improvement:        {summary['improvement']['percentage_improvement']:+.1f}%")
        
        print(f"\n🎯 PERFECT SCORES:")
        print(f"   Fine-tuned Model: {summary['fine_tuned']['perfect_scores']}/{len(results['fine_tuned'])}")
        print(f"   Base Model:       {summary['base_model']['perfect_scores']}/{len(results['base_model'])}")
        
        print(f"\n📈 CATEGORY PERFORMANCE:")
        for category, score in summary['fine_tuned']['category_scores'].items():
            base_score = summary['base_model']['category_scores'].get(category, 0)
            improvement = score - base_score
            print(f"   {category}: {score:.3f} (vs {base_score:.3f}, {improvement:+.3f})")
        
        # Detailed results
        print(f"\n📋 DETAILED RESULTS:")
        print("-" * 80)
        
        for i, (ft_result, bm_result) in enumerate(zip(results["fine_tuned"], results["base_model"])):
            print(f"\n{i+1}. {ft_result['category']} - {ft_result['difficulty'].upper()}")
            print(f"   Question: {ft_result['question']}")
            print(f"   Fine-tuned Score: {ft_result['score']:.3f} ({ft_result['matches']}/{ft_result['total_keywords']})")
            print(f"   Base Model Score: {bm_result['score']:.3f} ({bm_result['matches']}/{bm_result['total_keywords']})")
            print(f"   Response: {ft_result['response'][:100]}...")
            
            if ft_result['matched_keywords']:
                print(f"   Matched Keywords: {', '.join(ft_result['matched_keywords'])}")
    
    def save_results(self, results: Dict[str, Any], output_file: str):
        """Save evaluation results to file"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Results saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Evaluate fine-tuned memory insights model")
    parser.add_argument("base_model", help="Base model name (e.g., microsoft/DialoGPT-medium)")
    parser.add_argument("fine_tuned_model", help="Path to fine-tuned model directory")
    parser.add_argument("-o", "--output", default="evaluation_results.json",
                       help="Output file for results (default: evaluation_results.json)")
    parser.add_argument("--no-comparison", action="store_true",
                       help="Skip base model comparison")
    
    args = parser.parse_args()
    
    # Check if fine-tuned model exists
    if not Path(args.fine_tuned_model).exists():
        print(f"Error: Fine-tuned model directory '{args.fine_tuned_model}' not found")
        return 1
    
    try:
        # Initialize evaluator
        evaluator = MemoryInsightsEvaluator(args.base_model, args.fine_tuned_model)
        
        # Run evaluation
        results = evaluator.run_evaluation()
        
        # Print report
        evaluator.print_evaluation_report(results)
        
        # Save results
        evaluator.save_results(results, args.output)
        
        return 0
        
    except Exception as e:
        print(f"Error during evaluation: {e}")
        return 1

if __name__ == "__main__":
    exit(main())
