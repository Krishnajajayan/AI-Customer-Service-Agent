#  Customer Support Chatbot

A simple, interactive Gradio-based chatbot for handling common customer support tasks including FAQ responses, order tracking, small talk, and feedback collection.

---
## Backend
- **Data Loading**: Loads FAQs and order data from JSON files.
- **NLP**: Uses TF-IDF vectorization and cosine similarity to match user input with FAQs.
- **Order Status**: Matches order ID format `ORD123` and provides details.
- **Custom Logic**: Handles user queries for small talk, user info collection, and fallback responses.

## Frontend
- **UI Framework**: Built using Gradio for a simple, interactive chat interface.
- **Styling**: Custom CSS applied to style the chat and input fields.
- **Layout**: Organized using `gr.Row()` and `gr.Column()` components.

## How Frontend and Backend Work Together
- User input triggers the `respond()` function, which passes the message to the backend.
- The backend returns a response, which is displayed in the chat UI.
##  How to Run the Project

###  Prerequisites

Make sure you have the following installed:
- Python 3.8+
- pip
- Virtual environment (optional but recommended)

###  Install Dependencies

```bash
pip install -r requirements.txt
```
If you don't have a requirements.txt, you can install manually:

```bash
pip install gradio scikit-learn
```
###  Run the Chatbot

```bash
python main.py
```
The Gradio interface will launch in your browser. You can also use the ```share=True``` flag to share a public link.

###  Assumptions Made

- FAQs and orders are loaded from faqs.json and orders.json, which are expected to be present in the root directory.

- Order IDs follow the format ORD### (e.g., ORD123).

- User inputs like name and email are collected in a basic form, assuming the user types their real name and a valid email address.

- If no matching FAQ is found and it's not an order query or small talk, it escalates to a human representative.

###  Features Included

-  FAQ Matching using TF-IDF & fallback keyword logic.

-  Order Status Check by extracting order IDs from user input.

-  Small Talk: Handles greetings, thanks, goodbye, etc.

-  User Info Collection: Asks for name and email.

-  Clarification Prompts: Responds to vague queries like “why” with follow-up.

-  Fallback Handling: Escalates to human if input can't be handled.

-  Feedback Collection: Captures user feedback via UI.

-  Custom UI: Styled using custom CSS with a neat Gradio Blocks interface.
