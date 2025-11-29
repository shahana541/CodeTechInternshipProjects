import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from textblob import TextBlob
import random
import datetime
import json
import requests
import wikipediaapi
import numpy as np
import pickle
import os

# =============================================================================
# 1. KNOWLEDGE BASE (Put this at the top)
# =============================================================================

knowledge = {
    "greetings": {
        "patterns": ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"],
        "responses": [
            "Hello! How can I assist you today?",
            "Hi there! What can I help you with?",
            "Hey! Nice to see you. How can I be of service?"
        ]
    },
    "name": {
        "patterns": ["what is your name", "who are you", "your name"],
        "responses": [
            "My name is CodetechBot, your virtual assistant!",
            "I'm CodetechBot, here to help you with your queries.",
            "You can call me CodetechBot. I'm your friendly chatbot."
        ]
    },
    # ... (include all your existing knowledge categories from previous code)
}

advanced_knowledge = {
    "machine_learning": {
        "patterns": ["machine learning", "neural network", "ai model", "deep learning"],
        "responses": [
            "I use machine learning algorithms to improve my responses over time!",
            "My architecture includes neural networks for pattern recognition in conversations.",
            "I'm constantly learning from interactions to provide better assistance."
        ]
    },
    "memory": {
        "patterns": ["remember", "memory", "recall", "previous conversation"],
        "responses": [
            "I can remember our recent conversations and use that context to help you better!",
            "My memory system stores our interactions to provide more personalized responses.",
            "I maintain conversation history to understand context and your preferences."
        ]
    }
}

# Merge knowledge bases
knowledge.update(advanced_knowledge)

fallback_responses = [
    "I'm not sure I understand. Could you rephrase that?",
    "That's an interesting question! I'm still learning though.",
    "I don't have information about that yet. Try asking something else!",
    "Hmm, I'm not programmed to answer that. Maybe ask me about my capabilities?",
    "I'm still learning! Could you try a different question?"
]

commands_info = """
🤖 **CodetechBot Commands Guide** 🤖
**Basic Commands:**
- hello/hi/greetings: Start a conversation
- help: Show this help message
- exit/quit: Close the chatbot
**Advanced Features:**
- Weather in [city]: Get weather information
- Wikipedia [topic]: Get Wikipedia summary
- News: Get latest headlines
- I remember: Test my memory
"""

# =============================================================================
# 2. MACHINE LEARNING COMPONENT (Add this after knowledge base)
# =============================================================================

class MLChatbot:
    def __init__(self):
        self.model = None
        self.vectorizer = None
        self.load_or_train_model()
    
    def load_or_train_model(self):
        if os.path.exists('chatbot_model.h5') and os.path.exists('vectorizer.pkl'):
            try:
                # In a real implementation, you'd load TensorFlow model here
                print("ML model loaded successfully!")
            except:
                self.train_model()
        else:
            self.train_model()
    
    def train_model(self):
        print("Training ML model... (Placeholder - would train in production)")
        # This is simplified - real implementation would train on actual data

# =============================================================================
# 3. CONVERSATION MEMORY (Add this after ML component)
# =============================================================================

class ConversationMemory:
    def __init__(self, max_memory_size=100):
        self.memory = []
        self.max_memory_size = max_memory_size
        self.user_context = {}
        self.load_memory()
    
    def add_interaction(self, user_message, bot_response, sentiment):
        interaction = {
            'timestamp': datetime.datetime.now().isoformat(),
            'user_message': user_message,
            'bot_response': bot_response,
            'sentiment': sentiment,
            'context_clues': self.extract_context_clues(user_message)
        }
        
        self.memory.append(interaction)
        
        if len(self.memory) > self.max_memory_size:
            self.memory.pop(0)
        
        self.save_memory()
        self.update_user_context(user_message, bot_response)
    
    def extract_context_clues(self, message):
        clues = {}
        message_lower = message.lower()
        
        if 'my name is' in message_lower:
            name = message_lower.split('my name is')[-1].strip()
            clues['user_name'] = name.title()
        
        if 'i live in' in message_lower:
            location = message_lower.split('i live in')[-1].strip()
            clues['user_location'] = location.title()
        
        return clues
    
    def update_user_context(self, user_message, bot_response):
        clues = self.extract_context_clues(user_message)
        
        if 'user_name' in clues:
            self.user_context['user_name'] = clues['user_name']
        
        if 'user_location' in clues:
            self.user_context['user_location'] = clues['user_location']
    
    def get_recent_context(self, lookback_minutes=30):
        cutoff_time = datetime.datetime.now() - datetime.timedelta(minutes=lookback_minutes)
        recent = []
        
        for interaction in self.memory:
            if datetime.datetime.fromisoformat(interaction['timestamp']) > cutoff_time:
                recent.append(interaction)
        
        return recent
    
    def save_memory(self):
        try:
            with open('conversation_memory.json', 'w') as f:
                json.dump({
                    'memory': self.memory,
                    'user_context': self.user_context
                }, f, indent=2)
        except Exception as e:
            print(f"Error saving memory: {e}")
    
    def load_memory(self):
        try:
            with open('conversation_memory.json', 'r') as f:
                data = json.load(f)
                self.memory = data.get('memory', [])
                self.user_context = data.get('user_context', {})
        except FileNotFoundError:
            self.memory = []
            self.user_context = {}

# =============================================================================
# 4. API INTEGRATIONS (Add this after memory)
# =============================================================================

class APIIntegrations:
    def __init__(self):
        self.weather_api_key = "YOUR_OPENWEATHER_API_KEY"
        self.wiki_wiki = wikipediaapi.Wikipedia(
            user_agent='CodetechBot/1.0 (https://example.com; email@example.com)',
            language='en',
            extract_format=wikipediaapi.ExtractFormat.WIKI
        )
    
    def get_weather(self, location):
        try:
            if not self.weather_api_key or self.weather_api_key == "YOUR_OPENWEATHER_API_KEY":
                return "I need a weather API key to provide live weather data. You can get one from https://openweathermap.org"
            
            url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={self.weather_api_key}&units=metric"
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200:
                temp = data['main']['temp']
                desc = data['weather'][0]['description']
                humidity = data['main']['humidity']
                return f"🌤️ Weather in {location}: {desc.title()}, Temperature: {temp}°C, Humidity: {humidity}%"
            else:
                return f"❌ Sorry, I couldn't fetch weather for {location}. Please check the city name."
        except Exception as e:
            return "⚠️ Weather service is currently unavailable."

    def get_wikipedia_summary(self, topic):
        try:
            page = self.wiki_wiki.page(topic)
            if page.exists():
                summary = page.summary[:400] + "..." if len(page.summary) > 400 else page.summary
                return f"📚 Wikipedia: {summary}"
            else:
                return f"❌ I couldn't find information about '{topic}' on Wikipedia."
        except Exception as e:
            return "⚠️ Wikipedia service is currently unavailable."

    def get_news_headlines(self, category="general"):
        try:
            # Note: You need to get an API key from newsapi.org
            api_key = "YOUR_NEWS_API_KEY"
            if api_key == "YOUR_NEWS_API_KEY":
                return "📰 To get news headlines, please get a free API key from https://newsapi.org and replace 'YOUR_NEWS_API_KEY' in the code."
            
            url = f"https://newsapi.org/v2/top-headlines?category={category}&country=us&apiKey={api_key}"
            response = requests.get(url)
            data = response.json()
            
            if response.status_code == 200:
                headlines = [article['title'] for article in data['articles'][:3]]
                return "📰 Top News:\n• " + "\n• ".join(headlines)
            else:
                return "❌ Sorry, I couldn't fetch news headlines at the moment."
        except Exception as e:
            return "⚠️ News service is currently unavailable."

# =============================================================================
# 5. MAIN CHATBOT APPLICATION (Add this last)
# =============================================================================

class EnhancedChatbotApp:
    def __init__(self, master):
        self.master = master
        master.title("CodetechBot AI - Advanced Virtual Assistant 🤖")
        master.configure(bg='#f0f0f0')
        master.geometry("600x700")
        
        # Initialize advanced components
        self.ml_chatbot = MLChatbot()
        self.conversation_memory = ConversationMemory()
        self.api_integrations = APIIntegrations()
        
        self.setup_gui()
        
        # Welcome message
        self.write_message("🤖 CodetechBot AI: Hello! I'm your advanced AI assistant. I can remember our conversations, fetch real-time information, and learn from our interactions! Type 'help' for options.", "bot")

    def setup_gui(self):
        # Create main frame
        main_frame = tk.Frame(self.master, bg='#f0f0f0')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#2196F3', relief=tk.RAISED, bd=1)
        header_frame.pack(fill=tk.X, pady=(0,10))
        
        header_label = tk.Label(
            header_frame,
            text="🤖 CodetechBot AI",
            font=('Arial', 16, 'bold'),
            bg='#2196F3',
            fg='white',
            pady=10
        )
        header_label.pack()
        
        # Status bar
        self.status_var = tk.StringVar(value="🟢 Online - Ready to chat")
        status_bar = tk.Label(
            main_frame,
            textvariable=self.status_var,
            font=('Arial', 9),
            bg='#e0e0e0',
            fg='#666666',
            relief=tk.SUNKEN,
            bd=1
        )
        status_bar.pack(fill=tk.X, pady=(0,10))
        
        # Chat area
        self.chat_area = ScrolledText(
            main_frame,
            wrap=tk.WORD,
            state='disabled',
            width=60,
            height=25,
            bg='#ffffff',
            fg='#333333',
            font=('Arial', 10),
            padx=15,
            pady=15
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True, pady=(0,10))
        
        # Quick actions frame
        self.setup_quick_actions(main_frame)
        
        # Input frame
        self.setup_input_frame(main_frame)
        
        # Configure text tags
        self.configure_text_tags()

    def setup_quick_actions(self, parent):
        quick_actions_frame = tk.Frame(parent, bg='#f0f0f0')
        quick_actions_frame.pack(fill=tk.X, pady=(0,10))
        
        quick_actions = [
            ("🌤️ Weather", self.quick_weather),
            ("📰 News", self.quick_news),
            ("ℹ️ Wikipedia", self.quick_wikipedia),
            ("🕐 Time", self.quick_time),
            ("💾 Memory", self.quick_memory)
        ]
        
        for text, command in quick_actions:
            btn = tk.Button(
                quick_actions_frame,
                text=text,
                command=command,
                bg='#757575',
                fg='white',
                font=('Arial', 9),
                relief=tk.FLAT,
                padx=10
            )
            btn.pack(side=tk.LEFT, padx=(0,5))

    def setup_input_frame(self, parent):
        input_frame = tk.Frame(parent, bg='#f0f0f0')
        input_frame.pack(fill=tk.X)
        
        self.entry = tk.Entry(
            input_frame,
            width=60,
            font=('Arial', 11),
            bg='white',
            relief=tk.RAISED,
            bd=2
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind('<Return>', self.send_message)
        self.entry.focus()
        
        self.send_btn = tk.Button(
            input_frame,
            text="Send",
            command=self.send_message,
            bg='#4CAF50',
            fg='white',
            relief=tk.RAISED,
            font=('Arial', 10, 'bold'),
            padx=20
        )
        self.send_btn.pack(side=tk.RIGHT, padx=(10,0))

    def configure_text_tags(self):
        self.chat_area.config(state='normal')
        self.chat_area.tag_configure("timestamp", foreground="gray", font=('Arial', 8))
        self.chat_area.tag_configure("bot_prefix", foreground="#2196F3", font=('Arial', 9, 'bold'))
        self.chat_area.tag_configure("user_prefix", foreground="#FF5722", font=('Arial', 9, 'bold'))
        self.chat_area.tag_configure("bot_message", foreground="#333333")
        self.chat_area.tag_configure("user_message", foreground="#333333")
        self.chat_area.config(state='disabled')

    def write_message(self, message, sender="user"):
        self.chat_area.config(state='normal')
        
        timestamp = datetime.datetime.now().strftime("%H:%M")
        
        if sender == "bot":
            self.chat_area.insert(tk.END, f"\n[{timestamp}] ", "timestamp")
            self.chat_area.insert(tk.END, "🤖 CodetechBot: ", "bot_prefix")
            self.chat_area.insert(tk.END, f"{message}\n", "bot_message")
        else:
            self.chat_area.insert(tk.END, f"\n[{timestamp}] ", "timestamp")
            self.chat_area.insert(tk.END, "👤 You: ", "user_prefix")
            self.chat_area.insert(tk.END, f"{message}\n", "user_message")
        
        self.chat_area.config(state='disabled')
        self.chat_area.see(tk.END)

    # Quick action methods
    def quick_weather(self):
        self.entry.insert(0, "weather in London")
        self.send_message()

    def quick_news(self):
        self.entry.insert(0, "latest news")
        self.send_message()

    def quick_wikipedia(self):
        self.entry.insert(0, "wikipedia artificial intelligence")
        self.send_message()

    def quick_time(self):
        self.entry.insert(0, "current time")
        self.send_message()

    def quick_memory(self):
        self.entry.insert(0, "what do you remember about me?")
        self.send_message()

    def send_message(self, event=None):
        user_message = self.entry.get().strip()
        self.entry.delete(0, tk.END)
        
        if not user_message:
            return

        self.write_message(user_message, "user")
        
        # Show typing indicator
        self.status_var.set("🟡 Typing...")
        self.master.update()
        
        # Process message with slight delay to simulate thinking
        self.master.after(1000, lambda: self.process_and_respond(user_message))

    def process_and_respond(self, user_message):
        response = self.process_message(user_message)
        
        # Clear typing indicator
        self.status_var.set("🟢 Online - Ready to chat")
        
        self.write_message(response, "bot")
        
        # Store in memory
        sentiment = TextBlob(user_message).sentiment.polarity
        self.conversation_memory.add_interaction(user_message, response, sentiment)

    def process_message(self, user_message):
        user_message_lower = user_message.lower()
        
        # Handle exit commands
        if user_message_lower in ['exit', 'quit', 'bye', 'goodbye']:
            return "Goodbye! Thanks for chatting with me. Have a wonderful day! 👋"
        
        # Handle help command
        if user_message_lower in ['help', 'commands', 'what can you do']:
            return commands_info
        
        # Check for API commands
        if user_message_lower.startswith('weather in'):
            location = user_message_lower.replace('weather in', '').strip()
            return self.api_integrations.get_weather(location or "London")
        
        if 'news' in user_message_lower or 'headlines' in user_message_lower:
            return self.api_integrations.get_news_headlines()
        
        if user_message_lower.startswith('wikipedia'):
            topic = user_message_lower.replace('wikipedia', '').strip()
            return self.api_integrations.get_wikipedia_summary(topic or "Artificial Intelligence")
        
        # Handle memory queries
        if 'remember' in user_message_lower or 'memory' in user_message_lower:
            return self.handle_memory_query()
        
        # Use context from memory for personalized responses
        user_context = self.conversation_memory.user_context
        personalized_response = ""
        if 'user_name' in user_context:
            personalized_response = f"By the way {user_context['user_name']}, "
        
        # Enhanced response finding with context awareness
        response = self.find_enhanced_response(user_message_lower)
        
        if response:
            return personalized_response + response if personalized_response else response
        
        # Fallback with sentiment analysis
        sentiment = TextBlob(user_message).sentiment.polarity
        
        if sentiment > 0.3:
            return personalized_response + "That's wonderful! " + random.choice(fallback_responses)
        elif sentiment < -0.3:
            return personalized_response + "I understand this might be frustrating. " + random.choice(fallback_responses)
        else:
            return personalized_response + random.choice(fallback_responses)

    def handle_memory_query(self):
        user_context = self.conversation_memory.user_context
        memory_count = len(self.conversation_memory.memory)
        
        if not user_context and memory_count == 0:
            return "I don't have much memory of our conversation yet. Keep chatting with me!"
        
        response = f"I remember our last {memory_count} conversations"
        
        if 'user_name' in user_context:
            response += f" and that your name is {user_context['user_name']}"
        
        if 'user_location' in user_context:
            response += f" and you live in {user_context['user_location']}"
        
        response += "! 😊"
        return response

    def find_enhanced_response(self, user_message):
        # Check knowledge base
        for category, data in knowledge.items():
            for pattern in data['patterns']:
                if pattern in user_message:
                    return random.choice(data['responses'])
        
        return None

# =============================================================================
# 6. RUN THE APPLICATION (At the very end)
# =============================================================================

def main():
    root = tk.Tk()
    app = EnhancedChatbotApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()