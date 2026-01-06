from flask import Flask, request, jsonify, send_from_directory
from flask_login import LoginManager ,logout_user,login_user
from flask_cors import CORS
import os

from models import db, User, DanceClass, Subscriber, Review

from recommender import recommend_classes

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

app.config['SECRET_KEY'] = 'steezy_secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_request
def create_tables():
    with app.app_context():
        db.create_all()
        
from werkzeug.security import generate_password_hash, check_password_hash

# ---------------- HOME & FRONTEND ---------------- #

@app.route('/')
def home():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.static_folder, filename)

# ---------------- AUTH ---------------- #

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    hashed_password = generate_password_hash(data['password'])

    user = User(
        name=data['name'],
        email=data['email'],
        password=hashed_password
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()

    if user and check_password_hash(user.password, data['password']):
        login_user(user)
        return jsonify({
            "message": "Login successful",
            "name": user.name
        })
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/logout')
def logout():
    logout_user()
    return jsonify({"message": "Logged out"})

# ---------------- CLASSES API ---------------- #
@app.route('/ai-recommend', methods=['POST'])
def ai_recommend():
    data = request.json
    classes = DanceClass.query.all()
    return jsonify(
        recommend_classes(data['style'], data['level'], classes)
    )

@app.route('/classes')
def classes():
    classes = DanceClass.query.all()
    return jsonify([
        {
            "title": c.title,
            "level": c.level,
            "style": c.style
        } for c in classes
    ])

@app.route('/add-class', methods=['POST'])
def add_class():
    data = request.json
    new_class = DanceClass(
        title=data['title'],
        level=data['level'],
        style=data['style']
    )
    db.session.add(new_class)
    db.session.commit()
    return jsonify({"message": "Class added"})

# ---------------- NEWSLETTER ---------------- #

@app.route('/subscribe', methods=['POST'])
def subscribe():
    data = request.json
    sub = Subscriber(email=data['email'])
    db.session.add(sub)
    db.session.commit()
    return jsonify({"message": "Subscribed successfully"})

# ---------------- REVIEWS & RATINGS ---------------- #

@app.route('/reviews', methods=['GET'])
def get_reviews():
    reviews = Review.query.order_by(Review.created_at.desc()).all()
    return jsonify([
        {
            "id": r.id,
            "name": r.name,
            "text": r.text,
            "rating": r.rating,
            "created_at": r.created_at.isoformat() if r.created_at else None
        } for r in reviews
    ])

@app.route('/reviews', methods=['POST'])
def add_review():
    data = request.json
    review = Review(
        name=data['name'],
        text=data['text'],
        rating=data['rating']
    )
    db.session.add(review)
    db.session.commit()
    return jsonify({"message": "Review submitted successfully"})

# ---------------- AI CHATBOT ---------------- #

DANCE_KNOWLEDGE_BASE = {
    "hello": "Hi! 👋 Welcome to HC Dance Classes. How can I help you today?",
    "hi": "Hello! 🎉 Feel free to ask me about our dance styles, classes, levels, or any dance tips!",
    
    "styles": "We offer 4 main dance styles: 💃\n• Open Style - Express yourself freely\n• Hip Hop - Urban and energetic\n• Contemporary - Modern and artistic\n• Breaking - Dynamic and acrobatic",
    "style": "We offer 4 main dance styles: 💃\n• Open Style - Express yourself freely\n• Hip Hop - Urban and energetic\n• Contemporary - Modern and artistic\n• Breaking - Dynamic and acrobatic",
    
    "levels": "We have classes for all levels: 📊\n• BRAND NEW - Perfect if you have two left feet! Start with our 10-day intro\n• BEGINNER - You know the basics, ready to learn new moves\n• INTERMEDIATE - Feel confident and want more challenging skills\n• ADVANCED - Train with top choreographers in the game",
    "level": "We have classes for all levels: 📊\n• BRAND NEW - Perfect if you have two left feet! Start with our 10-day intro\n• BEGINNER - You know the basics, ready to learn new moves\n• INTERMEDIATE - Feel confident and want more challenging skills\n• ADVANCED - Train with top choreographers in the game",
    
    "hiphop": "Hip Hop is an urban and energetic dance style! 🎤\nIt's fun, expressive, and great for building confidence. Perfect for all levels!",
    "hip hop": "Hip Hop is an urban and energetic dance style! 🎤\nIt's fun, expressive, and great for building confidence. Perfect for all levels!",
    
    "contemporary": "Contemporary is a modern and artistic dance style! 🎨\nIt emphasizes emotional expression and freedom of movement. Great for developing your artistic side!",
    
    "breaking": "Breaking is dynamic and acrobatic! 🤸\nIt combines footwork, freezes, and power moves. Perfect if you want an exciting challenge!",
    
    "open style": "Open Style allows you to express yourself freely! 💫\nMix different styles, create your own moves, and develop your unique dance personality!",
    
    "beginner": "Perfect! As a beginner, you'll: ✨\n• Start with basic fundamentals\n• Learn proper technique and posture\n• Build confidence gradually\n• Join a supportive community of dancers",
    
    "intermediate": "Great choice for intermediate dancers! 🌟\nYou'll: • Challenge yourself with new moves\n• Learn choreographed routines\n• Improve your technique\n• Take on more complex skills",
    
    "advanced": "Awesome! Advanced dancers work with: 🏆\n• Top professional choreographers\n• Complex choreography\n• Performance opportunities\n• Specialized technique training",
    
    "sign up": "Ready to join? 🎉\nClick the 'Sign Up' button at the top right to create your account!\nYou'll get access to all our amazing classes!",
    "signup": "Ready to join? 🎉\nClick the 'Sign Up' button at the top right to create your account!\nYou'll get access to all our amazing classes!",
    
    "classes": "We offer 1500+ online dance classes! 💃\nChoose from different styles (Hip Hop, Contemporary, Breaking, Open Style) and levels (Brand New to Advanced). Start your journey today!",
    
    "cost": "We offer great value for quality dance education! 💰\nCheck our website for current pricing and special promotions like our New Year offer!",
    "price": "We offer great value for quality dance education! 💰\nCheck our website for current pricing and special promotions like our New Year offer!",
    "pricing": "We offer great value for quality dance education! 💰\nCheck our website for current pricing and special promotions like our New Year offer!",
    
    "contact": "Need to reach us? 📞\nOwner: Himanshu Choudhary\nPhone: 7300470078\nWe're here to help!",
    "owner": "Our founder is Himanshu Choudhary! 👤\nFeeling free to contact him at 7300470078 for any inquiries!",
    
    "community": "We have a global community of 100+ countries! 🌍\nOur dancers support each other, share tips, and take on dance challenges together. Join us!",
    
    "benefits": "Benefits of joining HC Dance Classes: ✨\n• Learn from expert choreographers\n• Flexible online classes\n• Supportive global community\n• Certificate programs\n• Affordable pricing",
    
    "help": "I can help you with: 🎯\n• Dance Styles - Ask about Hip Hop, Contemporary, Breaking, Open Style\n• Levels - Learn about Brand New, Beginner, Intermediate, Advanced\n• Classes - Find the right course for you\n• Contact - Get owner's details\n• Sign Up - Join our community\n• And much more!",
    "hello": "Hi there! 👋 Ask me about our dance styles, classes, levels, or anything else about dance!",
}

def get_chatbot_response(user_message):
    message = user_message.lower().strip()
    
    # Exact matches first
    if message in DANCE_KNOWLEDGE_BASE:
        return DANCE_KNOWLEDGE_BASE[message]
    
    # Keyword matching
    for key, response in DANCE_KNOWLEDGE_BASE.items():
        if key in message:
            return response
    
    # Default response
    return "Great question! 🤔 I can help with questions about dance styles, classes, levels, sign up, contact info, and more. Try asking about 'styles', 'levels', 'classes', or 'how to sign up'!"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({"response": "Please ask me something! 😊"})
    
    response = get_chatbot_response(user_message)
    return jsonify({"response": response})

# ---------------- RUN ---------------- #

if __name__ == '__main__':
    app.run(debug=True)
