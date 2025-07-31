#!/usr/bin/env python3
"""
Educational Chatbot - Final Year Project
A sophisticated AI-powered educational assistant with interactive features

Author: Student
Date: 2025
Purpose: Interactive learning companion for students

"Education is the most powerful weapon which you can use to change the world." - Nelson Mandela
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
import random
import json
import os
from datetime import datetime
import webbrowser
import re

class EducationalChatbot:
    """
    Main chatbot class implementing educational assistance with interactive UI
    
    Philosophy: "The best teachers are those who show you where to look, 
    but don't tell you what to see." - Alexandra K. Trenfor
    """
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_ui()
        self.setup_knowledge_base()
        self.conversation_history = []
        self.user_progress = {"questions_asked": 0, "topics_covered": set()}
        
    def setup_ui(self):
        """
        Create modern, interactive user interface
        Design principle: "Simplicity is the ultimate sophistication" - Leonardo da Vinci
        """
        self.root.title("🎓 Manu_EduBot - Your Learning Companion")
        self.root.geometry("900x700")
        self.root.configure(bg='#1a1a2e')
        
        # Modern styling
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Modern.TFrame', background='#16213e')
        style.configure('Modern.TLabel', background='#16213e', foreground='#ffffff')
        style.configure('Modern.TButton', background='#0f3460', foreground='#ffffff')
        
        # Header frame
        header_frame = ttk.Frame(self.root, style='Modern.TFrame')
        header_frame.pack(fill='x', padx=10, pady=5)
        
        title_label = ttk.Label(header_frame, text="🤖 EduBot - Interactive Learning Assistant", 
                               font=('Arial', 16, 'bold'), style='Modern.TLabel')
        title_label.pack(pady=10)
        
        # Status frame
        status_frame = ttk.Frame(self.root, style='Modern.TFrame')
        status_frame.pack(fill='x', padx=10)
        
        self.status_label = ttk.Label(status_frame, text="Ready to learn! Ask me anything...", 
                                     style='Modern.TLabel')
        self.status_label.pack(side='left')
        
        self.progress_label = ttk.Label(status_frame, text="Questions: 0 | Topics: 0", 
                                       style='Modern.TLabel')
        self.progress_label.pack(side='right')
        
        # Chat display area
        chat_frame = ttk.Frame(self.root, style='Modern.TFrame')
        chat_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame, 
            wrap=tk.WORD, 
            width=80, 
            height=25,
            bg='#0f1419',
            fg='#ffffff',
            font=('Consolas', 11),
            insertbackground='#ffffff'
        )
        self.chat_display.pack(fill='both', expand=True)
        
        # Input frame
        input_frame = ttk.Frame(self.root, style='Modern.TFrame')
        input_frame.pack(fill='x', padx=10, pady=5)
        
        self.user_input = tk.Entry(
            input_frame, 
            font=('Arial', 12),
            bg='#16213e',
            fg='#ffffff',
            insertbackground='#ffffff'
        )
        self.user_input.pack(side='left', fill='x', expand=True, padx=(0, 5))
        self.user_input.bind('<Return>', self.send_message)
        
        send_button = ttk.Button(input_frame, text="Send 📤", command=self.send_message)
        send_button.pack(side='right')
        
        # Quick action buttons
        action_frame = ttk.Frame(self.root, style='Modern.TFrame')
        action_frame.pack(fill='x', padx=10, pady=5)
        
        ttk.Button(action_frame, text="📚 Study Tips", 
                  command=lambda: self.quick_response("study_tips")).pack(side='left', padx=2)
        ttk.Button(action_frame, text="🧮 Math Help", 
                  command=lambda: self.quick_response("math")).pack(side='left', padx=2)
        ttk.Button(action_frame, text="🔬 Science", 
                  command=lambda: self.quick_response("science")).pack(side='left', padx=2)
        ttk.Button(action_frame, text="📖 Literature", 
                  command=lambda: self.quick_response("literature")).pack(side='left', padx=2)
        ttk.Button(action_frame, text="🌍 History", 
                  command=lambda: self.quick_response("history")).pack(side='left', padx=2)
        ttk.Button(action_frame, text="💡 Quiz Me", 
                  command=self.start_quiz).pack(side='right', padx=2)
        
        # Welcome message
        self.display_message("Manu_EduBot", "Welcome to your interactive learning journey! 🚀\n\n" +
                           "I'm here to help you with:\n" +
                           "• Subject explanations and concepts\n" +
                           "• Study techniques and tips\n" +
                           "• Interactive quizzes\n" +
                           "• Research guidance\n" +
                           "• Academic writing help\n\n" +
                           "Ask me anything or use the quick buttons below!")
        
    def setup_knowledge_base(self):
        """
        Initialize comprehensive educational knowledge base
        "Knowledge is power. Information is liberating." - Kofi Annan
        """
        self.knowledge_base = {
            "greetings": [
                "Hello! Ready to explore the world of knowledge? 🌟",
                "Hi there! What would you like to learn today? 📚",
                "Greetings, fellow learner! How can I assist your educational journey? 🎓"
            ],
            
            "study_tips": [
                "🎯 **Effective Study Techniques:**\n\n" +
                "1. **Pomodoro Technique**: 25 min study + 5 min break\n" +
                "2. **Active Recall**: Test yourself without looking at notes\n" +
                "3. **Spaced Repetition**: Review material at increasing intervals\n" +
                "4. **Feynman Technique**: Explain concepts in simple terms\n" +
                "5. **Mind Mapping**: Visual organization of information\n\n" +
                "💡 'The expert in anything was once a beginner.' - Helen Hayes"
            ],
            
            "math": {
                "algebra": "Algebra is the language of mathematics. Key concepts:\n• Variables and expressions\n• Equations and inequalities\n• Functions and graphs\n• Polynomials and factoring",
                "calculus": "Calculus studies continuous change:\n• Limits and continuity\n• Derivatives (rate of change)\n• Integrals (area under curves)\n• Applications in physics and engineering",
                "geometry": "Geometry explores shapes and space:\n• Points, lines, and planes\n• Angles and triangles\n• Circles and polygons\n• Area, perimeter, and volume"
            },
            
            "science": {
                "physics": "Physics explains how the universe works:\n• Motion and forces\n• Energy and momentum\n• Waves and optics\n• Electricity and magnetism\n• Quantum mechanics",
                "chemistry": "Chemistry studies matter and its interactions:\n• Atomic structure\n• Chemical bonds\n• Reactions and equations\n• Periodic table\n• Organic chemistry",
                "biology": "Biology explores life and living organisms:\n• Cell structure and function\n• Genetics and evolution\n• Ecology and ecosystems\n• Human anatomy and physiology"
            },
            
            "literature": [
                "📖 **Literary Analysis Tips:**\n\n" +
                "• **Theme**: Central message or meaning\n" +
                "• **Character Development**: How characters change\n" +
                "• **Setting**: Time and place significance\n" +
                "• **Symbolism**: Objects representing deeper meanings\n" +
                "• **Style**: Author's unique writing approach\n\n" +
                "'A reader lives a thousand lives before he dies.' - George R.R. Martin"
            ],
            
            "history": [
                "🏛️ **Historical Thinking Skills:**\n\n" +
                "• **Chronological Thinking**: Understanding time sequences\n" +
                "• **Historical Comprehension**: Analyzing sources\n" +
                "• **Analysis and Interpretation**: Drawing conclusions\n" +
                "• **Research Capabilities**: Finding reliable sources\n" +
                "• **Decision-Making**: Understanding cause and effect\n\n" +
                "'Those who cannot remember the past are condemned to repeat it.' - George Santayana"
            ],
            
            "quiz_questions": [
                {"question": "What is the derivative of x²?", "answer": "2x", "subject": "Math"},
                {"question": "Who wrote 'Romeo and Juliet'?", "answer": "William Shakespeare", "subject": "Literature"},
                {"question": "What is the chemical symbol for gold?", "answer": "Au", "subject": "Chemistry"},
                {"question": "In which year did World War II end?", "answer": "1945", "subject": "History"},
                {"question": "What is the speed of light?", "answer": "299,792,458 m/s", "subject": "Physics"}
            ]
        }
        
    def send_message(self, event=None):
        """
        Process user input and generate appropriate response
        "The important thing is not to stop questioning." - Albert Einstein
        """
        user_text = self.user_input.get().strip()
        if not user_text:
            return
            
        self.user_input.delete(0, tk.END)
        self.display_message("You", user_text)
        
        # Update progress
        self.user_progress["questions_asked"] += 1
        self.update_progress_display()
        
        # Show typing indicator
        self.show_typing_indicator()
        
        # Process response in separate thread
        threading.Thread(target=self.process_response, args=(user_text,), daemon=True).start()
        
    def process_response(self, user_text):
        """
        Generate intelligent response based on user input
        "Education is not preparation for life; education is life itself." - John Dewey
        """
        time.sleep(1)  # Simulate processing time
        
        response = self.generate_response(user_text.lower())
        
        # Update UI in main thread
        self.root.after(0, lambda: self.display_response(response))
        
    def generate_response(self, user_input):
        """
        Advanced response generation with pattern matching
        "The beautiful thing about learning is that no one can take it away from you." - B.B. King
        """
        # Greeting patterns
        if any(word in user_input for word in ['hello', 'hi', 'hey', 'greetings']):
            return random.choice(self.knowledge_base["greetings"])
            
        # Math-related queries
        elif any(word in user_input for word in ['math', 'mathematics', 'algebra', 'calculus', 'geometry']):
            self.user_progress["topics_covered"].add("Mathematics")
            if 'algebra' in user_input:
                return f"🧮 **Algebra Help:**\n\n{self.knowledge_base['math']['algebra']}\n\nNeed help with a specific algebra problem?"
            elif 'calculus' in user_input:
                return f"📊 **Calculus Concepts:**\n\n{self.knowledge_base['math']['calculus']}\n\nWhat calculus topic interests you?"
            elif 'geometry' in user_input:
                return f"📐 **Geometry Guide:**\n\n{self.knowledge_base['math']['geometry']}\n\nAny specific geometry questions?"
            else:
                return "🧮 **Mathematics Help Available:**\n\n• Algebra\n• Calculus\n• Geometry\n• Statistics\n• Trigonometry\n\nWhich area would you like to explore?"
                
        # Science queries
        elif any(word in user_input for word in ['science', 'physics', 'chemistry', 'biology']):
            self.user_progress["topics_covered"].add("Science")
            if 'physics' in user_input:
                return f"⚛️ **Physics Exploration:**\n\n{self.knowledge_base['science']['physics']}\n\nWhat physics concept can I explain?"
            elif 'chemistry' in user_input:
                return f"🧪 **Chemistry Insights:**\n\n{self.knowledge_base['science']['chemistry']}\n\nAny chemistry questions?"
            elif 'biology' in user_input:
                return f"🧬 **Biology Basics:**\n\n{self.knowledge_base['science']['biology']}\n\nWhat biological process interests you?"
            else:
                return "🔬 **Science Subjects:**\n\n• Physics - Laws of nature\n• Chemistry - Matter and reactions\n• Biology - Life sciences\n• Earth Science - Our planet\n\nWhich science fascinates you most?"
                
        # Study help
        elif any(word in user_input for word in ['study', 'learn', 'tips', 'help', 'technique']):
            self.user_progress["topics_covered"].add("Study Skills")
            return random.choice(self.knowledge_base["study_tips"])
            
        # Literature queries
        elif any(word in user_input for word in ['literature', 'book', 'novel', 'poem', 'writing']):
            self.user_progress["topics_covered"].add("Literature")
            return random.choice(self.knowledge_base["literature"])
            
        # History queries
        elif any(word in user_input for word in ['history', 'historical', 'past', 'ancient']):
            self.user_progress["topics_covered"].add("History")
            return random.choice(self.knowledge_base["history"])
            
        # Quiz request
        elif any(word in user_input for word in ['quiz', 'test', 'question', 'challenge']):
            return self.generate_quiz_question()
            
        # Default response with suggestions
        else:
            suggestions = [
                "🤔 I'd love to help! Try asking about:",
                "📚 **Subjects:** Math, Science, Literature, History",
                "💡 **Study Help:** Study tips, learning techniques",
                "🎯 **Interactive:** Quiz questions, practice problems",
                "🔍 **Specific Topics:** Algebra, Physics, Chemistry, etc.",
                "",
                "Example: 'Help me with calculus' or 'Give me study tips'"
            ]
            return "\n".join(suggestions)
            
    def generate_quiz_question(self):
        """Generate interactive quiz question"""
        question_data = random.choice(self.knowledge_base["quiz_questions"])
        self.current_quiz = question_data
        
        return f"🎯 **Quiz Time!**\n\n**Subject:** {question_data['subject']}\n**Question:** {question_data['question']}\n\nType your answer below!"
        
    def quick_response(self, topic):
        """Handle quick action button responses"""
        responses = {
            "study_tips": random.choice(self.knowledge_base["study_tips"]),
            "math": "🧮 **Mathematics Help:**\n\nWhat specific math topic would you like help with?\n• Algebra\n• Calculus\n• Geometry\n• Statistics\n• Trigonometry",
            "science": "🔬 **Science Assistance:**\n\nWhich science subject interests you?\n• Physics\n• Chemistry\n• Biology\n• Earth Science",
            "literature": random.choice(self.knowledge_base["literature"]),
            "history": random.choice(self.knowledge_base["history"])
        }
        
        self.display_message("EduBot", responses.get(topic, "How can I help you today?"))
        self.user_progress["topics_covered"].add(topic.replace("_", " ").title())
        self.update_progress_display()
        
    def start_quiz(self):
        """Start interactive quiz session"""
        self.display_message("EduBot", self.generate_quiz_question())
        
    def display_message(self, sender, message):
        """Display message in chat area with formatting"""
        timestamp = datetime.now().strftime("%H:%M")
        
        self.chat_display.config(state='normal')
        
        if sender == "You":
            self.chat_display.insert(tk.END, f"\n[{timestamp}] 👤 You: ", "user")
            self.chat_display.insert(tk.END, f"{message}\n", "user_msg")
        else:
            self.chat_display.insert(tk.END, f"\n[{timestamp}] 🤖 EduBot: ", "bot")
            self.chat_display.insert(tk.END, f"{message}\n", "bot_msg")
            
        # Configure text tags for styling
        self.chat_display.tag_config("user", foreground="#4CAF50", font=('Arial', 10, 'bold'))
        self.chat_display.tag_config("user_msg", foreground="#E8F5E8")
        self.chat_display.tag_config("bot", foreground="#2196F3", font=('Arial', 10, 'bold'))
        self.chat_display.tag_config("bot_msg", foreground="#E3F2FD")
        
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)
        
    def display_response(self, response):
        """Display bot response and hide typing indicator"""
        self.hide_typing_indicator()
        self.display_message("EduBot", response)
        
    def show_typing_indicator(self):
        """Show typing indicator"""
        self.status_label.config(text="🤖 EduBot is thinking...")
        
    def hide_typing_indicator(self):
        """Hide typing indicator"""
        self.status_label.config(text="Ready to help! Ask me anything...")
        
    def update_progress_display(self):
        """Update progress statistics"""
        questions = self.user_progress["questions_asked"]
        topics = len(self.user_progress["topics_covered"])
        self.progress_label.config(text=f"Questions: {questions} | Topics: {topics}")
        
    def run(self):
        """
        Start the educational chatbot application
        "Education is the passport to the future." - Malcolm X
        """
        self.root.mainloop()

def main():
    """
    Main function to initialize and run the Educational Chatbot
    
    Project Vision: "To create an interactive learning companion that makes 
    education accessible, engaging, and effective for every student."
    """
    print("🎓 Initializing Educational Chatbot...")
    print("📚 Loading knowledge base...")
    print("🚀 Starting interactive learning session...")
    
    try:
        chatbot = EducationalChatbot()
        chatbot.run()
    except Exception as e:
        print(f"❌ Error starting chatbot: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
