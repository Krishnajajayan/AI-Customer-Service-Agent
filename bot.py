import gradio as gr
import json
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load FAQs from a JSON file
with open("faqs.json") as f:
    faq_data = json.load(f)
faq_questions = [item["question"] for item in faq_data]
faq_answers = [item["answer"] for item in faq_data]

# Initialize TF-IDF Vectorizer and encode FAQ questions
vectorizer = TfidfVectorizer()
faq_vectors = vectorizer.fit_transform(faq_questions)

# Load order data from a JSON file
with open("orders.json") as f:
    orders = json.load(f)

# Store user information and feedback
user_info = {}
feedback_log = []

# Match user input with FAQs using semantic similarity
def get_faq_response(user_input):
    input_vec = vectorizer.transform([user_input])
    similarity = cosine_similarity(input_vec, faq_vectors)
    max_sim = similarity.max()
    if max_sim >= 0.5:
        index = similarity.argmax()
        return faq_answers[index]

    # Keyword-based fallback responses
    user_input_lower = user_input.lower()

    if any(kw in user_input_lower for kw in ["business hours", "working hours", "available", "what time", "till what time"]):
        return "Our business hours are 9 AM to 6 PM, Monday through Saturday."

    if "return" in user_input_lower:
        return "To return a product, go to your order history, select the product, and click 'Return'."

    if "international" in user_input_lower and "shipping" in user_input_lower:
        return "Yes, we ship to most countries worldwide. Shipping charges may apply."

    if "support" in user_input_lower or "contact" in user_input_lower:
        return "You can contact us at support@example.com or call 123-456-7890."

    if "payment" in user_input_lower or "methods" in user_input_lower:
        return "We accept Visa, MasterCard, PayPal, and UPI payments."

    if "address" in user_input_lower and "change" in user_input_lower:
        return "Yes, you can change the address within 12 hours of placing your order by contacting support."

    return None

# Extract and respond with order status using order ID
def get_order_status(user_input):
    match = re.search(r"\bORD\d+\b", user_input.upper())
    if match:
        order_id = match.group()
        for order in orders:
            if order["order_id"] == order_id:
                items = ", ".join(order["items"])
                return f"Order {order_id} is {order['status']}.\nItems: {items}\nExpected Delivery: {order['estimated_delivery']}"
        return f"No order found with ID {order_id}."

    if "order" in user_input.lower():
        return "Could you please provide your order ID (e.g., ORD123) so I can assist you with that?"

    return None

# Main chatbot response logic
def handle_input(user_input):
    user_input = user_input.strip()
    user_input_lower = user_input.lower()

    # Small talk responses
    if user_input_lower in ["hi", "hello"]:
        return "Hello! How can I assist you today?"
    if user_input_lower in ["thank you", "thanks"]:
        return "You're welcome!"
    if user_input_lower in ["bye", "goodbye"]:
        return "Goodbye! Have a great day!"
    if user_input_lower in ["no", "no thanks", "no thank you"]:
        return "Alright! Let me know if you need anything else."

    # Acknowledgment replies
    if user_input_lower in ["ok", "okay", "sure", "yes"]:
        return "Alright! Let me know if you have any more questions."

    # Clarification prompt
    if user_input_lower == "why":
        return "Could you please clarify what you're referring to? I'm here to help."

    # Check for name input (excluding common small talk words)
    greetings = ["good morning", "good afternoon", "good evening"]
    neutral_words = {"yes", "no", "ok", "okay", "sure", "thanks", "thank you", "hi", "hello", "bye", "goodbye", "why"}
    if user_input_lower not in greetings and re.match(r"^[A-Za-z ]+$", user_input) and "name" not in user_info and user_input_lower not in neutral_words:
        user_info["name"] = user_input
        return f"Thanks, {user_info['name']}. What's your email?"

    # Check for email input
    if "@" in user_input and "." in user_input and "email" not in user_info:
        user_info["email"] = user_input
        return f"Thanks for sharing your email{', ' + user_info['name'] if 'name' in user_info else ''}."

    # Try order status
    order_response = get_order_status(user_input)
    if order_response:
        return order_response

    # Try FAQ matching
    faq_response = get_faq_response(user_input)
    if faq_response:
        return faq_response

    # Fallback message
    return "I'm not sure how to help with that. Let me connect you with a human representative."

# Collect feedback from user
def collect_feedback(feedback_text):
    if feedback_text.strip():
        feedback_log.append(feedback_text)
        return "Thanks for your feedback!"
    else:
        return "Please enter some feedback before submitting."

# Gradio UI setup
with gr.Blocks() as demo:
    # App title
    gr.Markdown("""
    # 🤖 Customer Support Chatbot
    Welcome to our support assistant. Type your query and get instant help!
    """)

    # Custom styling
    custom_css = """
    body {
        background-color: #f0f4f8;
        font-family: 'Segoe UI', sans-serif;
    }
    #chatbox {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 12px;
        height: 400px;
        overflow-y: auto;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    .chat-input-wrapper {
        position: relative;
        width: 100%;
        margin-top: 10px;
    }
    #message-input {
        border-radius: 25px;
        padding: 12px 45px 12px 15px;
        width: 100%;
        border: 1px solid #cccccc;
        font-size: 16px;
        background-color: #fefefe;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.05);
    }
    #message-input:focus {
        border-color: #66afe9;
        outline: none;
        box-shadow: 0 0 5px rgba(102,175,233,0.6);
    }
    #send-btn {
        position: absolute;
        top: 50%;
        right: 10px;
        transform: translateY(-50%);
        background-color: #4caf50;
        color: white;
        border: none;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        font-size: 20px;
        cursor: pointer;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2);
    }
    #send-btn:hover {
        background-color: #45a049;
    }
    #feedback-section {
        background-color: #fffbe7;
        border-radius: 10px;
        padding: 15px;
        margin-top: 25px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }
    #feedback-section textarea {
        background-color: #ffffff;
        border-radius: 10px;
        border: 1px solid #ddd;
        padding: 10px;
    }
    #feedback-section button {
        background-color: #2196f3;
        color: white;
        border: none;
        padding: 8px 16px;
        border-radius: 6px;
        margin-top: 8px;
        cursor: pointer;
        font-weight: bold;
    }
    #feedback-section button:hover {
        background-color: #1976d2;
    }
    """
    gr.HTML(f"<style>{custom_css}</style>")

    # Chat history display
    chatbot = gr.Chatbot(type="messages", elem_id="chatbox")

    # Input textbox and send button
    with gr.Row():
        with gr.Column():
            gr.HTML('<div class="chat-input-wrapper">')
            msg = gr.Textbox(label="", elem_id="message-input", placeholder="Type your message...")
            send_btn = gr.Button("➡", elem_id="send-btn")
            gr.HTML('</div>')

    # Feedback section
    with gr.Column(elem_id="feedback-section"):
        gr.Markdown("### 💬 Feedback")
        feedback = gr.Textbox(label="Your Feedback", placeholder="Share your feedback here...", lines=2)
        feedback_btn = gr.Button("Submit Feedback")

    # Update chat based on message
    def respond(message, chat_history):
        response = handle_input(message)
        chat_history.append({"role": "user", "content": message})
        chat_history.append({"role": "assistant", "content": response})
        return "", chat_history

    # Event bindings
    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    send_btn.click(respond, [msg, chatbot], [msg, chatbot])
    feedback_btn.click(collect_feedback, feedback, feedback)

    # Launch the app
    demo.launch(share=True)
