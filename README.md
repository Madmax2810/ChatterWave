# **ChatterWave**  

ChatterWave is a session-based web chat application that enables real-time communication with built-in voice-to-text transcription. It offers an intuitive interface for seamless chat interactions and supports audio-based messaging, ensuring users can send voice inputs conveniently.  

---

## **Features**  
- **Voice-to-Text (VTT) Transcription:**  
  Users can record audio messages, which are transcribed into text within the chat interface.  
- **Session-Based Communication:**  
  Join or create chat rooms using a unique session ID to manage focused conversations effectively.  
- **Real-Time Messaging:**  
  Instant message exchange for uninterrupted communication across sessions.

---

## **Technologies Used**  

### **Frontend:**  
- **HTML5** and **CSS3:** Structure and styling of the chat interface.  
- **JavaScript** (with **Socket.IO**): Handles real-time messaging and user interactions.  

### **Backend:**  
- **Flask (Python):** Powers the backend for user sessions and message management.  
- **Vosk:** Provides voice-to-text transcription, converting voice inputs into readable text.  

### **Deployment & Environment:**  
- **Virtual Environment (env):** Manages project dependencies in isolation.  
- **Socket.IO:** Enables real-time communication between the frontend and backend.  

---

## **How to Run the Project Locally**  

1. **Clone the Repository:**  
   ```bash
   git clone <repository-url>
   cd ChatterWave
   ```
2. **Set up Virtual Environment:**
  ```bash
    python -m venv env
    source env/bin/activate    # On Linux/macOS  
    env\Scripts\activate       # On Windows
  ```
3. **Install Dependencies:**
  ```bash
  pip install -r requirements.txt
  ```
4. **Run the Flask Server:**
  ```bash
  python app.py

  
