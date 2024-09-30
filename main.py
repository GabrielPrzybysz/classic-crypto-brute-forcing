from flask import Flask, request, render_template_string

app = Flask(__name__)

def create_hashset(path):
    hashset = set()
    with open(path, 'r') as file:
        for line in file:
            word = line.strip()
            hashset.add(word)
    return hashset

hashset = create_hashset('./words.txt')

def brute_caesar(word):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    word = word.lower()
    possible_decryptions = []

    for shift in range(1, 26):
        decrypted_word = ''
        for char in word:
            if char in alphabet:
                shifted_index = (alphabet.index(char) - shift) % 26
                decrypted_word += alphabet[shifted_index]
            else:
                decrypted_word += char
        possible_decryptions.append((shift, decrypted_word))
    
    return possible_decryptions

def format_decryptions(possible_decryptions):
    found_words = []
    other_words = []
    
    for shift, word in possible_decryptions:
        if word in hashset:
            found_words.append((shift, word))
        else:
            other_words.append((shift, word))
    
    # Prioritize found words by placing them at the top
    prioritized_decryptions = found_words + other_words
    
    result = ""
    for shift, word in prioritized_decryptions:
        color = "green" if word in hashset else "black"
        result += f"<h3 style=\"color:{color};\"> Key: {shift}, word: {word} </h3> <br>"
    
    return result

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        uploaded_file = request.files['file']
        if uploaded_file and uploaded_file.filename.endswith('.txt'):
            content = uploaded_file.read().decode('utf-8')
            first_line = content.splitlines()[0]
            result = brute_caesar(first_line)
            return format_decryptions(result)
    return render_template_string('''
        <html>
            <body style="font-family: Arial, sans-serif; margin: 20px;">
                <h1 style="color: #333;">Cifra de César Brute Force</h1>
                <form method="post" enctype="multipart/form-data">
                    <input type="file" name="file" accept=".txt" required style="margin-bottom: 10px;">
                    <input type="submit" value="Enviar" style="padding: 5px 10px; background-color: #007BFF; color: white; border: none; border-radius: 5px; cursor: pointer;">
                </form>
            </body>
        </html>
    ''')
