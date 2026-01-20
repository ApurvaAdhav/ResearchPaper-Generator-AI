import os
from groq import Groq

class PaperGenerator:
    def __init__(self, api_key=None, model_name='llama-3.3-70b-versatile'):
        self.api_key = api_key
        if api_key:
            self.client = Groq(api_key=api_key)
            self.model_name = model_name
        else:
            self.client = None
            self.model_name = model_name

    def _get_mock_content(self, section, inputs):
        """Returns placeholder content if no API key is provided."""
        return f"[MOCK CONTENT FOR {section} - NO API KEY PROVIDED]\n\n" + \
               f"Please enter a valid Groq API Key to generate real research content for '{inputs.get('title', 'Untitled')}'.\n" + \
               "Groq offers very fast inference with Llama 3 models."

    def generate_section(self, section_name, inputs, prev_context=""):
        """
        Generates a specific section of the paper using Groq API.
        """
        if not self.client:
             return self._get_mock_content(section_name, inputs)

        prompt = self._construct_prompt(section_name, inputs, prev_context)
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a strict academic assistant. Output purely the content of the research paper section requested."
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.model_name,
                temperature=0.5,
                max_tokens=4096,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Error generating {section_name} with Groq: {str(e)}"

    def _construct_prompt(self, section, inputs, prev_context):
        base_instruction = (
            "You are a PhD-level research scientist aimed at publishing in a top-tier IEEE/Nature journal. "
            "Your task is to write a HIGHLY DETAILED, technically dense, and extensive section for a research paper. "
            "Do not write brief summaries. Iterate deeply on the concepts. "
            "Write ONLY the content for the requested section. Do not include the section title. "
        )

        specific_instructions = {
            "Abstract": "Write a dense 350-500 word Abstract. Cover: Context/Background, Specific Problem Gap, The Novel Methodology (in technical detail), The Quantitative Results (give specific numbers), and Impact.",
            "Introduction": (
                "Write a 1500-word deep-dive Introduction. "
                "1. Broad Context (300 words). "
                "2. Specific Technical Challenges (400 words). "
                "3. In-depth analysis of the Research Gap (400 words). "
                "4. Major Contributions (bullet points). "
                "Cite references frequently as [1], [2]."
            ),
            "Literature Review": (
                "Write a major 2000-word Literature Review. "
                "Group similar works into sub-themes (e.g., 'Early Statistical Methods', 'Deep Learning Approaches'). "
                "For each paper cited, explain its method, its finding, and specifically its LIMITATION. "
                "You MUST include a markdown comparison table with 8+ rows comparing methods on features, accuracy, and latency."
            ),
            "Methodology": (
                "Write a massive 2000-word Technical Methodology. "
                "This must be the core of the paper. "
                "1. Mathematical Model (include equations in LaTeX format like $E=mc^2$). "
                "2. System Architecture (describe every module in extreme detail). "
                "3. Algorithm Construction (provide pseudo-code steps). "
                "4. Implementation Details (hyperparameters, environment)."
            ),
            "Results and Discussion": (
                "Write a 1500-word Results section. "
                "1. Experimental Setup (Datasets, Hardware). "
                "2. Metrics Defined (Precision, Recall, F1, etc.). "
                "3. Quantitative Analysis (Compare your proposed method vs SOTA). "
                "4. Ablation Studies (What happens if we remove module X?). "
            ),
            "Conclusion": "Write a 500-word Conclusion summarizing the technical achievements and strictly defining the limitations and future scope.",
            "Future Work": "Elaborate on 3 specific directions for future research in detail.",
            "References": (
                "Generate exactly 20 high-quality references in IEEE format. "
                "Diverse years (2018-2024). "
                "CRITICAL: Every reference must end with a [Link] or DOI."
            )
        }

        user_context = (
            f"Title: {inputs['title']}\n"
            f"Domain: {inputs['domain']}\n"
            f"Problem: {inputs['problem']}\n"
            f"Style: Highly Technical, PhD-Level, Extensive\n"
        )

        return f"{base_instruction}\n\nContext:\n{user_context}\n\nTask: Write the '{section}' section.\n{specific_instructions.get(section, '')}"
