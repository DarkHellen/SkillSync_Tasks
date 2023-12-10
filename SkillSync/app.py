from flask import Flask, render_template, request, jsonify
import re
import math

app = Flask(__name__)

def calculate_entropy(password):
    char_set = 0
    entropy = 0

    # Count character set
    if re.search(r"[a-z]", password):
        char_set += 26
    if re.search(r"[A-Z]", password):
        char_set += 26
    if re.search(r"\d", password):
        char_set += 10
    if re.search(r"\W", password):
        char_set += 32

    # Calculate entropy
    entropy = math.log2(char_set) * len(password)
    return entropy

def calculate_score(password):
    score = 0

    # Add points for various characteristics
    if re.search(r"[a-z]", password):
        score += 1
    if re.search(r"[A-Z]", password):
        score += 1
    if re.search(r"\d", password):
        score += 1
    if re.search(r"\W", password):
        score += 2
    if len(password) >= 8:
        score += 2

    return score

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_password_strength', methods=['POST'])
def check_password_strength():
    password = request.form.get('password', '')
    
    # Check for common passwords (you may want to use a more extensive list)
    common_passwords = ['password', '123456', 'qwerty']
    if password.lower() in common_passwords:
        return jsonify({'message': 'Common password. Please choose a stronger one.'})

    entropy = calculate_entropy(password)
    score = calculate_score(password)

    return jsonify({'entropy': entropy, 'score': score})

if __name__ == '__main__':
    app.run(debug=True)
