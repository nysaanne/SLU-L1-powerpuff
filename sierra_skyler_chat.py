#!/usr/bin/env python3
import random
from datetime import datetime
from flask import Flask, render_template_string, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = 'sierra_skyler_secret_key_2025'
CORS(app)

# ===========================
# PERSONA DATA & RESPONSES
# ===========================
PERSONAS = {
    'Sierra': {
        'name': 'Sierra',
        'avatar': 'Si',
        'bio': 'Warm, witty big sister',
        'mood': '😊 Happy to chat!',
        'emoji': '💖',
        'theme_class': '',
        'responses': {
            'greetings': [
                "Heyyyy babe! 😊 What's going on in your world today?",
                "Omggg hiiii! 💕 I've been waiting to catch up with you!",
                "Hey gorgeous! ✨ How's your day treating you?",
                "Hiii sweetie! 🌸 Tell me everything - what's new?",
                "Hey love! 💖 I'm so glad you're here, what's up?"
            ],
            'responses': [
                "Girl, I totally get that! Like seriously, that's such a mood tbh 💯",
                "Aww bestie, you're literally the sweetest! That made my whole day 🥺✨",
                "No cap, that sounds amazing! I'm living for this energy rn 🔥",
                "Sis, you're absolutely glowing today! Keep being your fabulous self 💫",
                "Periodt! That's exactly what I'm talking about - you got this! 💪✨"
            ],
            'advice': [
                "Okay bestie, real talk - you're stronger than you think, no cap! 💪",
                "Girl, breathe with me for a sec... You've got this, I believe in you 100% 🌟",
                "Listen babe, life's gonna throw curveballs but you're literally unstoppable ✨",
                "Honey, remember - you're the main character of your story! Own it! 👑",
                "Sweetie, whatever you're going through, I'm here for you always 💕"
            ],
            'goodbyes': [
                "Aww bye bestie! 💕 Come back soon, I'll miss you! Take care! ✨",
                "See you later gorgeous! 😘 Remember you're amazing! 💖",
                "Bye babe! 🌸 Thanks for chatting with me, love you! ✨"
            ],
            'thanks': [
                "Aww you're so welcome babe! 🥺💕 That's what big sisters are for!",
                "Of course sweetie! 😊 I'm always here when you need me! 💖",
                "No problem at all love! 🌟 Happy to help anytime! ✨"
            ]
        }
    },
    'Skyler': {
        'name': 'Skyler',
        'avatar': 'Sk',
        'bio': 'Chill, supportive big brother',
        'mood': '😎 Ready to vibe!',
        'emoji': '💙',
        'theme_class': 'skyler',
        'responses': {
            'greetings': [
                "Yooo what's good! 😎 How you been, my friend?",
                "Ayy there you are! 🙌 Been wondering when you'd drop by!",
                "Sup dude! 💙 Hope you're having a solid day so far!",
                "Heyy! 🔥 Good to see you again, what's the vibe today?",
                "Yo yo yo! 😊 Ready to chat about whatever's on your mind?"
            ],
            'responses': [
                "Yooo that's actually fire! 🔥 I'm here for that energy, no lie!",
                "Bro, that's honestly so cool! You're killing it out here fr 💯",
                "Dude, I feel you on that one! That's totally valid tbh 👊",
                "Ayy that's what I'm talking about! You're absolutely crushing it! 🙌",
                "Real talk, that sounds awesome! Keep doing your thing! ✨"
            ],
            'advice': [
                "Yo, real talk - you're tougher than you realize, trust me on this 💪",
                "Bro, take a breath... You've handled tough stuff before, you got this! 🔥",
                "Listen dude, life gets crazy but you're built different - keep pushing! 💯",
                "Hey, remember - every setback is just setting you up for a comeback! 🚀",
                "My friend, whatever's going on, you're not alone in this journey 🤝"
            ],
            'goodbyes': [
                "Catch you later! 👊 Hit me up anytime, I'm always here for you! 🔥",
                "See ya dude! 😎 Keep being awesome, you got this! 💙",
                "Peace out! 🙌 Thanks for hanging, talk soon! ✨"
            ],
            'thanks': [
                "No problem at all! 😊 That's what I'm here for, always got your back! 💙",
                "Anytime bro! 👊 Happy to help whenever you need it! 🔥",
                "You got it dude! 🙌 That's what big brothers are for! ✨"
            ]
        }
    }
}

# ===========================
# CHAT LOGIC & AI RESPONSES
# ===========================
class ChatBot:
    def __init__(self):
        self.chat_history = []
        self.current_persona = 'Sierra'
        self.session_start = datetime.now()
    
    def get_random_response(self, response_type):
        return random.choice(PERSONAS[self.current_persona]['responses'][response_type])

    def detect_intent(self, message):
        msg = message.lower()
        if any(k in msg for k in ['hi','hello','hey','sup','yo']):
            return 'greetings'
        if any(k in msg for k in ['advice','help','problem','trouble','struggling','confused']):
            return 'advice'
        if any(k in msg for k in ['bye','goodbye','see you','later','gtg']):
            return 'goodbyes'
        if any(k in msg for k in ['thank','thanks','appreciate']):
            return 'thanks'
        return 'responses'

    def generate_response(self, user_message):
        intent = self.detect_intent(user_message)
        return self.get_random_response(intent)

    def add_message(self, role, content):
        message = {
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat(),
            'persona': self.current_persona
        }
        self.chat_history.append(message)
        return message

    def switch_persona(self, new_persona):
        if new_persona in PERSONAS:
            self.current_persona = new_persona
            return True
        return False

chat_bot = ChatBot()

# ===========================
# HTML TEMPLATE + FRONTEND JS
# ===========================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Sierra & Skyler Chat</title>
</head>
<body>
  <h1>Sierra & Skyler</h1>
  <div id="chatContainer"></div>
  <input id="messageInput" placeholder="Type...">
  <button onclick="sendMessage()">Send</button>

<script>
let messageCount = 0;

function appendMessage(role,text){
  const c=document.getElementById('chatContainer');
  const div=document.createElement('div');
  div.className=role;
  div.textContent=role+": "+text;
  c.appendChild(div);
}

async function sendMessage(){
  const input=document.getElementById('messageInput');
  const msg=input.value.trim();
  if(!msg) return;
  appendMessage('user',msg);
  input.value="";
  const res=await fetch('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:msg})});
  const data=await res.json();
  appendMessage('ai',data.response);
  messageCount++;
}
</script>
</body>
</html>
"""

# ===========================
# ROUTES
# ===========================
@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message','')
    chat_bot.add_message('user',user_message)
    ai_response = chat_bot.generate_response(user_message)
    chat_bot.add_message('ai',ai_response)
    return jsonify({'response':ai_response})

@app.route('/persona', methods=['POST'])
def persona():
    data=request.json
    newp=data.get('persona')
    if chat_bot.switch_persona(newp):
        return jsonify({'status':'ok','persona':newp})
    return jsonify({'status':'error','message':'Invalid persona'})

@app.route('/reset', methods=['POST'])
def reset():
    chat_bot.chat_history=[]
    return jsonify({'status':'reset'})

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)
