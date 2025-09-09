#!/usr/bin/env python3
"""
Memory Insights Training Data Extractor

This script extracts training examples from your memory.md file
and converts them into instruction-following format for LLM fine-tuning.
"""

import json
import re
import argparse
from pathlib import Path
from typing import List, Dict, Any

class MemoryInsightsExtractor:
    def __init__(self, memory_file_path: str):
        self.memory_file_path = memory_file_path
        self.content = self._load_content()
        self.examples = []
    
    def _load_content(self) -> str:
        """Load memory.md content"""
        with open(self.memory_file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def extract_all_examples(self) -> List[Dict[str, Any]]:
        """Extract all training examples from memory"""
        self.examples = []
        
        # Extract different types of insights
        self._extract_architecture_patterns()
        self._extract_environment_gotchas()
        self._extract_critical_commands()
        self._extract_lessons_learned()
        self._extract_authentication_info()
        self._extract_environment_config()
        
        return self.examples
    
    def _extract_architecture_patterns(self):
        """Extract architecture pattern examples"""
        patterns_section = self._extract_section("## Architecture Patterns Discovered")
        if not patterns_section:
            return
        
        # Field Implementation Patterns
        field_patterns = re.findall(
            r'- \*\*(.*?)\*\*: (.*?)(?=\n-|\n\n|$)', 
            patterns_section, 
            re.DOTALL
        )
        
        for pattern_name, description in field_patterns:
            self.examples.append({
                "instruction": f"What is the {pattern_name} and how should I implement it?",
                "context": "I'm working on a GraphQL/Prisma/React application with PostgreSQL database",
                "response": f"The {pattern_name}: {description.strip()}"
            })
        
        # GraphQL Resolver Priority
        resolver_section = self._extract_section("### GraphQL Resolver Priority", patterns_section)
        if resolver_section:
            resolver_points = re.findall(r'- \*\*(.*?)\*\*: (.*?)(?=\n-|\n\n|$)', resolver_section, re.DOTALL)
            for point_name, explanation in resolver_points:
                self.examples.append({
                    "instruction": f"How do GraphQL resolvers work in this codebase?",
                    "context": "I'm implementing GraphQL resolvers and need to understand the priority system",
                    "response": f"{point_name}: {explanation.strip()}"
                })
        
        # UI Conditional Rendering Patterns
        ui_section = self._extract_section("### UI Conditional Rendering Patterns", patterns_section)
        if ui_section:
            ui_patterns = re.findall(r'- \*\*(.*?)\*\*: (.*?)(?=\n-|\n\n|$)', ui_section, re.DOTALL)
            for pattern_name, description in ui_patterns:
                self.examples.append({
                    "instruction": f"How should I handle {pattern_name.lower()} in the UI?",
                    "context": "I'm implementing UI components and need to understand rendering patterns",
                    "response": f"For {pattern_name}: {description.strip()}"
                })
    
    def _extract_environment_gotchas(self):
        """Extract environment gotcha examples"""
        gotchas_section = self._extract_section("## Environment Gotchas")
        if not gotchas_section:
            return
        
        # Extract subsections
        subsections = re.findall(r'### (.*?)\n(.*?)(?=\n### |$)', gotchas_section, re.DOTALL)
        
        for section_name, content in subsections:
            # Extract bullet points
            bullets = re.findall(r'- \*\*(.*?)\*\*: (.*?)(?=\n-|\n\n|$)', content, re.DOTALL)
            
            for gotcha_name, solution in bullets:
                self.examples.append({
                    "instruction": f"I'm having issues with {gotcha_name.lower()}. What should I do?",
                    "context": f"I'm working on {section_name.lower()} in my development environment",
                    "response": f"For {gotcha_name}: {solution.strip()}"
                })
    
    def _extract_critical_commands(self):
        """Extract critical command examples"""
        commands_section = self._extract_section("## Critical Commands")
        if not commands_section:
            return
        
        # Extract command sections
        command_sections = re.findall(r'### (.*?)\n(.*?)(?=\n### |$)', commands_section, re.DOTALL)
        
        for section_name, content in command_sections:
            # Extract code blocks
            code_blocks = re.findall(r'```bash\n(.*?)\n```', content, re.DOTALL)
            
            if code_blocks:
                combined_commands = '\n'.join(code_blocks)
                self.examples.append({
                    "instruction": f"How do I {section_name.lower()}?",
                    "context": "I need to execute commands for development environment management",
                    "response": f"For {section_name}:\n```bash\n{combined_commands.strip()}\n```"
                })
    
    def _extract_lessons_learned(self):
        """Extract lessons learned examples"""
        lessons_section = self._extract_section("## Key Lessons Learned")
        if not lessons_section:
            return
        
        # Extract subsections
        subsections = re.findall(r'### (.*?)\n(.*?)(?=\n### |$)', lessons_section, re.DOTALL)
        
        for section_name, content in subsections:
            # Extract bullet points
            bullets = re.findall(r'- \*\*(.*?)\*\*: (.*?)(?=\n-|\n\n|$)', content, re.DOTALL)
            
            for lesson_name, explanation in bullets:
                self.examples.append({
                    "instruction": f"What should I know about {lesson_name.lower()}?",
                    "context": f"I'm following {section_name.lower()} methodology",
                    "response": f"{lesson_name}: {explanation.strip()}"
                })
    
    def _extract_authentication_info(self):
        """Extract authentication information examples"""
        auth_section = self._extract_section("## Authentication Information")
        if not auth_section:
            return
        
        # Working Credentials
        creds_section = self._extract_section("### Working Credentials", auth_section)
        if creds_section:
            creds = re.findall(r'- \*\*(.*?)\*\*: (.*?)(?=\n-|\n\n|$)', creds_section, re.DOTALL)
            for cred_name, value in creds:
                self.examples.append({
                    "instruction": f"What are the working authentication credentials?",
                    "context": "I need to access the application for testing",
                    "response": f"{cred_name}: {value.strip()}"
                })
        
        # Access Requirements
        access_section = self._extract_section("### Access Requirements", auth_section)
        if access_section:
            requirements = re.findall(r'- \*\*(.*?)\*\*: (.*?)(?=\n-|\n\n|$)', access_section, re.DOTALL)
            for req_name, description in requirements:
                self.examples.append({
                    "instruction": f"What are the access requirements for this application?",
                    "context": "I'm setting up access to the application",
                    "response": f"{req_name}: {description.strip()}"
                })
    
    def _extract_environment_config(self):
        """Extract environment configuration examples"""
        config_section = self._extract_section("## Environment Configuration")
        if not config_section:
            return
        
        # Extract configuration sections
        config_sections = re.findall(r'### (.*?)\n(.*?)(?=\n### |$)', config_section, re.DOTALL)
        
        for section_name, content in config_sections:
            # Extract environment variables
            env_vars = re.findall(r'([A-Z_]+)=([^\n]+)', content)
            
            if env_vars:
                env_list = [f"{var}={value}" for var, value in env_vars]
                self.examples.append({
                    "instruction": f"How do I configure {section_name.lower()}?",
                    "context": "I'm setting up environment variables for development",
                    "response": f"For {section_name}, set these environment variables:\n" + "\n".join(env_list)
                })
    
    def _extract_section(self, header: str, content: str = None) -> str:
        """Extract a section from the content"""
        if content is None:
            content = self.content
        
        pattern = rf"{re.escape(header)}(.*?)(?=\n## |$)"
        match = re.search(pattern, content, re.DOTALL)
        return match.group(1).strip() if match else ""
    
    def save_training_data(self, output_file: str, format: str = "jsonl"):
        """Save training data to file"""
        if format == "jsonl":
            with open(output_file, 'w', encoding='utf-8') as f:
                for example in self.examples:
                    f.write(json.dumps(example, ensure_ascii=False) + '\n')
        elif format == "json":
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(self.examples, f, indent=2, ensure_ascii=False)
        
        print(f"Saved {len(self.examples)} training examples to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Extract training data from memory.md")
    parser.add_argument("memory_file", help="Path to memory.md file")
    parser.add_argument("-o", "--output", default="training_data.jsonl", 
                       help="Output file path (default: training_data.jsonl)")
    parser.add_argument("-f", "--format", choices=["jsonl", "json"], default="jsonl",
                       help="Output format (default: jsonl)")
    
    args = parser.parse_args()
    
    # Check if memory file exists
    if not Path(args.memory_file).exists():
        print(f"Error: Memory file '{args.memory_file}' not found")
        return 1
    
    # Extract training data
    extractor = MemoryInsightsExtractor(args.memory_file)
    examples = extractor.extract_all_examples()
    
    if not examples:
        print("No training examples extracted. Check your memory.md format.")
        return 1
    
    # Save training data
    extractor.save_training_data(args.output, args.format)
    
    print(f"\nExtraction Summary:")
    print(f"- Total examples: {len(examples)}")
    print(f"- Output format: {args.format}")
    print(f"- Output file: {args.output}")
    
    return 0

if __name__ == "__main__":
    exit(main())
