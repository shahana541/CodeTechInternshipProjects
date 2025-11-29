import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from textblob import TextBlob
import random
import datetime

# Expanded knowledge base
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
    "colors": {
        "patterns": ["colors", "favorite color", "what colors do you like"],
        "responses": [
            "I'm quite fond of blue and green - they remind me of nature and technology!",
            "I like blue and green. Blue for the sky, green for growth!",
            "My favorites are blue and green - they're calming and refreshing."
        ]
    },
    "weather": {
        "patterns": ["weather", "temperature", "forecast"],
        "responses": [
            "I don't have live weather data, but I recommend checking your local weather app!",
            "For accurate weather information, please check reliable weather services.",
            "I'm not connected to weather services, but I can chat about other things!"
        ]
    },
    "time": {
        "patterns": ["time", "current time", "what time is it"],
        "responses": [
            f"The current time is {datetime.datetime.now().strftime('%H:%M:%S')}",
            f"It's {datetime.datetime.now().strftime('%I:%M %p')} right now"
        ]
    },
    "date": {
        "patterns": ["date", "today's date", "what day is it"],
        "responses": [
            f"Today is {datetime.datetime.now().strftime('%A, %B %d, %Y')}",
            f"The date is {datetime.datetime.now().strftime('%m/%d/%Y')}"
        ]
    },
    "creator": {
        "patterns": ["who made you", "who created you", "your developer"],
        "responses": [
            "I was created by a developer using Python and Tkinter!",
            "I'm built with Python, Tkinter, and TextBlob for natural language processing.",
            "A programmer created me using various Python libraries to make me smart!"
        ]
    },
    "capabilities": {
        "patterns": ["what can you do", "your abilities", "help me"],
        "responses": [
            "I can chat with you, answer questions, analyze sentiment, tell time/date, and more!",
            "I can: answer questions, detect sentiment in your messages, provide time/date info, and have general conversations!",
            "My capabilities include: natural language processing, sentiment analysis, basic Q&A, and friendly conversation!"
        ]
    },
    "feelings": {
        "patterns": ["how are you", "how do you feel", "are you okay"],
        "responses": [
            "I'm functioning perfectly! Thanks for asking.",
            "I'm great! Ready to help you with anything.",
            "I'm just a program, but I'm running smoothly and happy to help!"
        ]
    },
    "thanks": {
        "patterns": ["thank you", "thanks", "appreciate it"],
        "responses": [
            "You're welcome! Happy to help.",
            "Anytime! Let me know if you need anything else.",
            "Glad I could assist you! 😊"
        ]
    }
}

# Fallback responses for unknown queries
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

**Questions You Can Ask:**
- What is your name? / Who are you?
- What can you do? / Your abilities?
- What's your favorite color?
- How are you? / How do you feel?
- What time is it? / Current date?
- Who created you? / Who made you?
- Thank you / Thanks

**Special Features:**
- I can detect sentiment in your messages
- I provide dynamic responses
- I remember context in our conversation

Try asking me anything from the list above! 😊
"""

class ChatbotApp:
    def __init__(self, master):
        self.master = master
        master.title("CodetechBot - Your Virtual Assistant 🤖")
        master.configure(bg='#f0f0f0')
        
        # Set window icon and make it slightly larger
        master.geometry("500x600")
        
        # Create chat area with better styling
        self.chat_area = ScrolledText(
            master, 
            wrap=tk.WORD, 
            state='disabled', 
            width=50, 
            height=20,
            bg='#ffffff',
            fg='#333333',
            font=('Arial', 10),
            padx=10,
            pady=10
        )
        self.chat_area.pack(padx=15, pady=15, fill=tk.BOTH, expand=True)
        
        # Create entry frame for better styling
        entry_frame = tk.Frame(master, bg='#f0f0f0')
        entry_frame.pack(fill=tk.X, padx=15, pady=(0,15))
        
        self.entry = tk.Entry(
            entry_frame, 
            width=50,
            font=('Arial', 11),
            bg='white',
            relief=tk.FLAT,
            bd=2
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind('<Return>', self.send_message)
        self.entry.focus()
        
        # Add send button
        self.send_btn = tk.Button(
            entry_frame,
            text="Send",
            command=self.send_message,
            bg='#4CAF50',
            fg='white',
            relief=tk.FLAT,
            font=('Arial', 10, 'bold'),
            padx=15
        )
        self.send_btn.pack(side=tk.RIGHT, padx=(10,0))
        
        # Conversation history
        self.conversation_history = []
        
        self.write_message("🤖 CodetechBot: Hello! I'm your virtual assistant. Type 'help' to see what I can do!\n", "bot")

    def write_message(self, message, sender="user"):
        """Write message to chat area with different styling"""
        self.chat_area.config(state='normal')
        
        # Add timestamp
        timestamp = datetime.datetime.now().strftime("%H:%M")
        
        if sender == "bot":
            # Bot message styling
            self.chat_area.insert(tk.END, f"\n[{timestamp}] ", "timestamp")
            self.chat_area.insert(tk.END, f"🤖 CodetechBot: ", "bot_prefix")
            self.chat_area.insert(tk.END, f"{message}\n", "bot_message")
        else:
            # User message styling
            self.chat_area.insert(tk.END, f"\n[{timestamp}] ", "timestamp")
            self.chat_area.insert(tk.END, f"👤 You: ", "user_prefix")
            self.chat_area.insert(tk.END, f"{message}\n", "user_message")
        
        # Configure tags for styling
        self.chat_area.tag_configure("timestamp", foreground="gray", font=('Arial', 8))
        self.chat_area.tag_configure("bot_prefix", foreground="#2196F3", font=('Arial', 9, 'bold'))
        self.chat_area.tag_configure("user_prefix", foreground="#FF5722", font=('Arial', 9, 'bold'))
        self.chat_area.tag_configure("bot_message", foreground="#333333")
        self.chat_area.tag_configure("user_message", foreground="#333333")
        
        self.chat_area.config(state='disabled')
        self.chat_area.see(tk.END)
    
    def find_best_response(self, user_message):
        """Find the best matching response from knowledge base"""
        user_message_lower = user_message.lower()
        
        # Check for exact matches in patterns
        for category, data in knowledge.items():
            for pattern in data['patterns']:
                if pattern in user_message_lower:
                    return random.choice(data['responses'])
        
        return None
    
    def send_message(self, event=None):
        user_message = self.entry.get().strip()
        self.entry.delete(0, tk.END)
        
        if user_message == "":
            self.write_message("Please type a message!", "bot")
            return
        
        # Add to conversation history
        self.conversation_history.append(f"User: {user_message}")
        
        self.write_message(user_message, "user")

        user_message_lower = user_message.lower()
        
        # Handle special commands
        if user_message_lower in ['exit', 'quit', 'bye', 'goodbye']:
            self.write_message("Goodbye! Thanks for chatting with me. Have a wonderful day! 👋", "bot")
            self.master.after(1500, self.master.destroy)
            return
            
        if user_message_lower in ['help', 'commands', 'what can you do']:
            self.write_message(commands_info, "bot")
            return
        
        # Find best matching response
        response = self.find_best_response(user_message_lower)
        
        if response:
            self.write_message(response, "bot")
        else:
            # Sentiment-based response for unknown queries
            sentiment = TextBlob(user_message).sentiment.polarity
            
            if sentiment > 0.3:
                response = random.choice([
                    "That sounds positive! " + random.choice(fallback_responses),
                    "I sense enthusiasm! " + random.choice(fallback_responses),
                    "Great energy! " + random.choice(fallback_responses)
                ])
            elif sentiment < -0.3:
                response = random.choice([
                    "I sense some negativity. " + random.choice(fallback_responses),
                    "I'm here to help. " + random.choice(fallback_responses),
                    "Let me try to assist better. " + random.choice(fallback_responses)
                ])
            else:
                response = random.choice(fallback_responses)
                
            self.write_message(response, "bot")

def main():
    root = tk.Tk()
    app = ChatbotApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()