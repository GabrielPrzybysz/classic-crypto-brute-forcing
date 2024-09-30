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
    result = ""
    for shift, word in possible_decryptions:
        if word in hashset:
            result += f"<h3 style=\"color:green\"> Key: {shift}, word: {word} </h3> <br>"
        else:
            result += f"<h3> Key: {shift}, word: {word} </h3> <br>"
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
            <body>
                <h1>Cifra de César Brute Force</h1>
                <form method="post" enctype="multipart/form-data">
                    <input type="file" name="file" accept=".txt" required>
                    <input type="submit" value="Enviar">
                </form>
            </body>
        </html>
    ''')
