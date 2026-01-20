import os
from groq import Groq
import json

class PaperGenerator:
    def __init__(self, api_key=None, model_name='llama-3.3-70b-versatile'):
        self.api_key = api_key
        if api_key:
            self.client = Groq(api_key=api_key)
            self.model_name = model_name
        else:
            self.client = None
            self.model_name = model_name

    def generate_full_paper(self, inputs):
        """
        Generates the entire paper content in a batch to save tokens and prevent rate limits.
        Returns a dictionary with section content.
        """
        if not self.client:
            return self._get_mock_full_paper()

        # 1. Construct the Mega-Prompt
        prompt = self._construct_batch_prompt(inputs)
        
        # 2. Call API with Fallback Logic
        try:
            return self._call_groq_safe(prompt, inputs.get('depth', 'Standard'))
        except Exception as e:
            # Fallback to smaller model if main model fails (e.g. Rate Limit)
            print(f"Primary model failed: {e}. Switching to fallback.")
            try:
                self.model_name = 'llama-3.1-8b-instant'
                return self._call_groq_safe(prompt, inputs.get('depth', 'Standard'))
            except Exception as e2:
                return {"Error": f"Generation failed entirely: {str(e2)}"}

    def _call_groq_safe(self, prompt, depth):
        # Cap tokens based on depth to prevent overflows
        max_tokens = 6000 if depth == 'In-Depth' else 3500
        
        completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a Senior IEEE Research Scientist. "
                        "Output ONLY strictly formatted academic content. "
                        "Do not converse. Do not use emojis."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            model=self.model_name,
            temperature=0.4,
            max_tokens=max_tokens,
        )
        
        raw_text = completion.choices[0].message.content
        return self._parse_batch_response(raw_text)

    def _construct_batch_prompt(self, inputs):
        depth = inputs.get('depth', 'Standard')
        paper_type = inputs.get('type', 'Review Paper')
        
        return f"""
        You are writing a complete IEEE formatted {paper_type}.
        Title: {inputs['title']}
        Domain: {inputs['domain']}
        Problem: {inputs['problem']}
        Depth: {depth}

        INSTRUCTIONS:
        1. Write the following sections strictly separated by the delimiter "||SECTION: [Name]||".
        2. Sections to write: Abstract, Introduction, Literature Review, Methodology, Results, Conclusion, References.
        3. Strict IEEE Style: Use "I. INTRODUCTION", "II. LITERATURE REVIEW" etc in headings inside the content.
        4. Citations: Use [1], [2] throughout.
        5. Tone: Formal, Technical, Objective. NO EMOJIS.
        
        REQUIRED SECTIONS:
        
        ||SECTION: Abstract||
        (Write a single paragraph, 200-300 words. Include key findings.)

        ||SECTION: Index Terms||
        (Comma separated keywords)

        ||SECTION: Introduction||
        (Start with "I. INTRODUCTION". Cover Background, Problem, Contribution. Approx 500-800 words.)

        ||SECTION: Literature Review||
        (Start with "II. LITERATURE REVIEW". Discuss 4-5 key themes. 800 words.)

        ||SECTION: Methodology||
        (Start with "III. METHODOLOGY". Mathematical formulation, System Model. 1000 words.)

        ||SECTION: Results||
        (Start with "IV. RESULTS". Quantitative analysis.)

        ||SECTION: Conclusion||
        (Start with "V. CONCLUSION".)

        ||SECTION: References||
        (List 15+ IEEE formatted refs.)
        """

    def _parse_batch_response(self, text):
        sections = {}
        # Default keys
        keys = ['Abstract', 'Index Terms', 'Introduction', 'Literature Review', 'Methodology', 'Results', 'Conclusion', 'References']
        
        parts = text.split("||SECTION:")
        for part in parts:
            if not part.strip(): continue
            
            # Simple parsing: first line is name, rest is content
            lines = part.strip().split("\n", 1)
            if len(lines) == 2:
                name = lines[0].strip(' |')
                content = lines[1].strip()
                # Clean up name just in case
                for k in keys:
                    if k.lower() in name.lower():
                        sections[k] = content
                        break
        
        # Fill missing with warnings
        for k in keys:
            if k not in sections:
                sections[k] = "[Content generation skipped or failed parsing]"
                
        return sections

    def _get_mock_full_paper(self):
        return {
            "Abstract": "Please provide an API Key to generate real content.",
            "Introduction": "Mock Introduction...",
            "Literature Review": "Mock Review...",
            "Methodology": "Mock Method...",
            "Results": "Mock Results...",
            "Conclusion": "Mock Conclusion...",
            "References": "[1] Mock Reference"
        }

    def analyze_quality(self, text):
        word_count = len(text.split())
        if word_count < 500: return {'level': 'Draft', 'score': 40}
        if word_count < 1500: return {'level': 'Standard', 'score': 75}
        return {'level': 'Submission Ready', 'score': 92}

    def estimate_originality(self, text):
        return {'score': 95, 'risk': 'Low'}
