# abcd-agentic-training-vnr-akshithnani17

1. Business ProblemResearchers, students, and professionals are overwhelmed by the sheer volume of academic publications. Standard LLM summaries often result in "walls of text" that miss nuances, fail to distinguish between methodology and results, or lose context in long-form PDFs (20+ pages). There is a need for a system that parses, analyzes, and critiques papers with the same rigor as a human reader.


2. Possible SolutionA single-prompt approach often suffers from "lost in the middle" context issues. A Multi-Agent Workflow solves this by:Role Specialization: Assigning specific tasks (parsing, reasoning, formatting) to different agent personas.Context Management: Breaking the paper into manageable chunks (Map-Reduce) to ensure no critical data is dropped.Structured Output: Enforcing a consistent schema for every summary generated.

  
3. Implemented SolutionThis project implements a three-tier agentic architecture:The Reader (Parser): High-fidelity extraction using PyMuPDF, specifically targeting headers to maintain document hierarchy.The Analyst (Summarizer): A logic-driven agent that evaluates the methodology and results.The Editor (Final Polish): A formatting agent that ensures the output adheres to a specific "One-Sentence Value Prop" and "Critical Limitations" structure.

4. Tech Stack UsedOrchestration: LangGraph (for stateful, multi-agent coordination).LLM: Gemini 1.


5. Pro (utilized for its 2M token context window and multimodal capabilities).PDF Engine: PyMuPDF (fast, reliable text and table extraction).Environment: Python 3.10+, Docker. Architecture DiagramThe system follows a sequential and iterative flow to ensure quality control.


6. How to Run LocallyClone the Repository:Bashgit clone https://github.com/akshithnani17/AI-Research-Paper-.git
cd ai-research-summarizer
Set Up Environment:Bashpython -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
Configure API Keys:Create a .env file and add your Google Gemini API Key:Code snippetGOOGLE_API_KEY=your_api_key_here
Launch the Application:Bashpython main.py --path ./papers/sample_paper.pdf

7. References and ResourcesLangGraph DocumentationGemini API - Long Context PromptingAttention Is All You Need (Sample paper used for testing).


8. ScreenshotsInput (PDF Upload)Agent Logs (Processing)Final Structured Summary![Upload UI]![Terminal Output]![Final Report]
   

10. Alignment and FormattingThis project adheres to PEP 8 standards for Python code and uses Markdown for documentation to ensure cross-platform compatibility and readability.

11. Problems Faced and SolutionsProblemSolutionPDF Tables: Raw text extraction turned tables into gibberish.Implemented Multimodal Analysis—the Reader agent now sends snapshots of complex tables to Gemini 1.5 Pro for visual interpretation.Token Limits: Very long papers caused "Map" agents to lose the "big picture."Implemented a Global State Object in LangGraph that stores the "Abstract" context, making it accessible to all agents regardless of which section they are currently summarizing.Hallucinated Limits: Agents sometimes invented limitations not in the text.Added a Verification Step where the Editor agent must cite a specific section from the "Reader's" raw notes to justify a "Critical Limitation."
