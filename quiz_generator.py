import streamlit as st
import re
import random
from typing import List, Dict, Tuple

class QuizGenerator:
    def __init__(self):
        self.question_starters = [
            "What is the significance of",
            "How does",
            "Why is",
            "What are the main characteristics of",
            "Explain the relationship between",
            "What factors contribute to",
            "How can we understand",
            "What role does"
        ]
        
        self.essay_prompts = [
            "Analyze and discuss the key concepts presented in the text regarding {}. Provide specific examples and explain their significance.",
            "Compare and contrast different aspects of {} mentioned in the document. How do these elements relate to each other?",
            "Evaluate the importance of {} in the context provided. What are the potential implications or consequences?",
            "Describe the main themes related to {} and explain how they connect to broader concepts or real-world applications.",
            "Critically examine {} as presented in the text. What questions or areas for further research does this raise?"
        ]
    
    def extract_key_terms(self, text: str) -> List[str]:
        """Extract key terms from the text using simple heuristics."""
        # Remove common words and extract meaningful terms
        common_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these',
            'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him',
            'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their'
        }
        
        # Split into sentences and words
        sentences = re.split(r'[.!?]+', text)
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        
        # Count word frequency
        word_freq = {}
        for word in words:
            if word not in common_words:
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Get most frequent terms (at least 2 occurrences)
        key_terms = [word for word, freq in word_freq.items() if freq >= 2]
        
        # If not enough frequent terms, add some single occurrence terms
        if len(key_terms) < 10:
            single_terms = [word for word, freq in word_freq.items() if freq == 1]
            key_terms.extend(single_terms[:10-len(key_terms)])
        
        return key_terms[:15]  # Return top 15 terms
    
    def extract_sentences(self, text: str) -> List[str]:
        """Extract meaningful sentences from the text."""
        sentences = re.split(r'[.!?]+', text)
        meaningful_sentences = []
        
        for sentence in sentences:
            sentence = sentence.strip()
            # Filter out very short sentences
            if len(sentence.split()) >= 5:
                meaningful_sentences.append(sentence)
        
        return meaningful_sentences
    
    def generate_essay_questions(self, text: str, key_terms: List[str]) -> List[str]:
        """Generate essay assignment questions."""
        essay_questions = []
        
        # Use top key terms for essay topics
        selected_terms = key_terms[:3] if len(key_terms) >= 3 else key_terms
        
        for i, term in enumerate(selected_terms[:2]):  # Generate 2 questions
            prompt_template = random.choice(self.essay_prompts)
            question = prompt_template.format(term)
            essay_questions.append(f"Essay Question {i+1}: {question}")
        
        # If we don't have enough key terms, generate generic questions
        while len(essay_questions) < 2:
            generic_question = f"Essay Question {len(essay_questions)+1}: Analyze the main ideas presented in the provided text and discuss their significance. Support your analysis with specific examples from the material."
            essay_questions.append(generic_question)
        
        return essay_questions
    
    def generate_multiple_choice(self, text: str, key_terms: List[str], sentences: List[str]) -> List[Dict]:
        """Generate multiple choice questions."""
        mc_questions = []
        
        # Generate questions based on key terms and sentences
        for i in range(3):  # Generate 3 questions
            if i < len(key_terms) and i < len(sentences):
                term = key_terms[i]
                context_sentence = sentences[i] if i < len(sentences) else sentences[0]
                
                question_starter = random.choice(self.question_starters)
                question = f"{question_starter} {term}?"
                
                # Generate options (this is simplified - in a real application, 
                # you might use NLP libraries for better option generation)
                correct_answer = f"Related to {term} as mentioned in the context"
                
                options = [
                    correct_answer,
                    f"Unrelated concept A about {random.choice(key_terms) if key_terms else 'general topic'}",
                    f"Unrelated concept B about {random.choice(key_terms) if key_terms else 'another topic'}",
                    f"Unrelated concept C about {random.choice(key_terms) if key_terms else 'different subject'}"
                ]
                
                # Shuffle options
                random.shuffle(options)
                correct_index = options.index(correct_answer)
                
                mc_questions.append({
                    'question': question,
                    'options': options,
                    'correct_answer': chr(65 + correct_index),  # A, B, C, or D
                    'explanation': f"This question focuses on understanding {term} in the given context."
                })
            else:
                # Generic question if we run out of terms
                question = f"What is a key concept discussed in the text?"
                options = [
                    "A main idea from the provided material",
                    "An unrelated concept",
                    "A different topic entirely", 
                    "Something not mentioned in the text"
                ]
                
                mc_questions.append({
                    'question': question,
                    'options': options,
                    'correct_answer': 'A',
                    'explanation': "This question tests comprehension of the main content."
                })
        
        return mc_questions
    
    def generate_content(self, input_text: str) -> Tuple[List[str], List[Dict]]:
        """Main method to generate all content."""
        if not input_text.strip():
            return [], []
        
        # Extract key information from text
        key_terms = self.extract_key_terms(input_text)
        sentences = self.extract_sentences(input_text)
        
        # Generate content
        essay_questions = self.generate_essay_questions(input_text, key_terms)
        mc_questions = self.generate_multiple_choice(input_text, key_terms, sentences)
        
        return essay_questions, mc_questions

def main():
    st.set_page_config(
        page_title="Assignment & Quiz Generator",
        page_icon="📝",
        layout="wide"
    )
    
    st.title("📝 Assignment & Quiz Generator")
    st.markdown("Generate essay questions and multiple-choice quizzes from any document or topic!")
    
    # Initialize the generator
    if 'generator' not in st.session_state:
        st.session_state.generator = QuizGenerator()
    
    # Sidebar for instructions
    with st.sidebar:
        st.header("📋 Instructions")
        st.markdown("""
        1. **Enter your text** in the input area
        2. **Click 'Generate'** to create questions
        3. **Review** the generated assignments and quiz
        4. **Copy** or export the results as needed
        
        **Tips:**
        - Longer texts produce better results
        - Include key concepts and detailed information
        - The generator works with any subject matter
        """)
        
        st.header("⚙️ Settings")
        show_explanations = st.checkbox("Show quiz explanations", value=True)
    
    # Main input area
    st.header("📄 Input Text or Topic")
    
    # Text input options
    input_method = st.radio("Choose input method:", ["Type/Paste Text", "Upload File"])
    
    input_text = ""
    
    if input_method == "Type/Paste Text":
        input_text = st.text_area(
            "Enter your document content or topic description:",
            height=200,
            placeholder="Paste your document content here or describe a topic you want to create questions about..."
        )
    else:
        uploaded_file = st.file_uploader(
            "Upload a text file (.txt)",
            type=['txt'],
            help="Upload a plain text file containing your document content"
        )
        
        if uploaded_file is not None:
            input_text = str(uploaded_file.read(), "utf-8")
            st.text_area("File content preview:", value=input_text[:500] + "..." if len(input_text) > 500 else input_text, height=150, disabled=True)
    
    # Generate button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        generate_clicked = st.button("🔄 Generate Questions", type="primary", use_container_width=True)
    
    # Generate and display results
    if generate_clicked and input_text.strip():
        with st.spinner("Generating questions..."):
            essay_questions, mc_questions = st.session_state.generator.generate_content(input_text)
        
        if essay_questions or mc_questions:
            st.success("Questions generated successfully!")
            
            # Display results in two columns
            col1, col2 = st.columns(2)
            
            # Essay Questions
            with col1:
                st.header("📚 Assignment Questions")
                if essay_questions:
                    for i, question in enumerate(essay_questions, 1):
                        st.subheader(f"Question {i}")
                        st.write(question.replace(f"Essay Question {i}: ", ""))
                        st.markdown("---")
                else:
                    st.info("No essay questions generated.")
            
            # Multiple Choice Questions
            with col2:
                st.header("❓ Quiz Questions")
                if mc_questions:
                    for i, q in enumerate(mc_questions, 1):
                        st.subheader(f"Question {i}")
                        st.write(q['question'])
                        
                        for j, option in enumerate(q['options']):
                            prefix = chr(65 + j)  # A, B, C, D
                            if prefix == q['correct_answer']:
                                st.write(f"**{prefix}. {option}** ✓")
                            else:
                                st.write(f"{prefix}. {option}")
                        
                        st.write(f"**Correct Answer: {q['correct_answer']}**")
                        
                        if show_explanations:
                            st.write(f"*Explanation: {q['explanation']}*")
                        
                        st.markdown("---")
                else:
                    st.info("No quiz questions generated.")
            
            # Export options
            st.header("📤 Export Results")
            
            # Prepare export text
            export_text = "ASSIGNMENT & QUIZ GENERATOR RESULTS\n" + "="*50 + "\n\n"
            
            export_text += "ASSIGNMENT QUESTIONS:\n" + "-"*25 + "\n"
            for i, question in enumerate(essay_questions, 1):
                export_text += f"\n{i}. {question.replace(f'Essay Question {i}: ', '')}\n"
            
            export_text += "\n\nQUIZ QUESTIONS:\n" + "-"*20 + "\n"
            for i, q in enumerate(mc_questions, 1):
                export_text += f"\n{i}. {q['question']}\n"
                for j, option in enumerate(q['options']):
                    prefix = chr(65 + j)
                    export_text += f"   {prefix}. {option}\n"
                export_text += f"   Correct Answer: {q['correct_answer']}\n"
                if show_explanations:
                    export_text += f"   Explanation: {q['explanation']}\n"
            
            # Download button
            st.download_button(
                label="📥 Download Results as Text File",
                data=export_text,
                file_name="quiz_and_assignments.txt",
                mime="text/plain"
            )
            
        else:
            st.error("Could not generate questions from the provided text. Please try with more detailed content.")
    
    elif generate_clicked:
        st.warning("Please enter some text before generating questions.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "💡 Tip: The quality of generated questions improves with longer, more detailed input text."
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()