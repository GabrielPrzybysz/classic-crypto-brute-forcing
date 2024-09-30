from flask import Flask

app = Flask(__name__)

hashset = create_hashset('./words.txt')
alphabet = 'abcdefghijklmnopqrstuvwxyz'

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400

    file = request.files['file']

    if file.filename == '':
        return "No selected file", 400

    if file:
        file_content = file.read().decode('utf-8')
        
        first_word = file_content.split()[0] if file_content else None

        return f"The first word is: {first_word}"

def brute_caesar(word):
    word = word.lower()
    
    possible_decryptions = []
    
    for shift in range(26):
        decrypted_word = ''
        
        for char in word:
            if char in alphabet:
                shifted_index = (alphabet.index(char) - shift) % 26
                decrypted_word += alphabet[shifted_index]
            else:
                decrypted_word += char
        
        possible_decryptions.append((shift, decrypted_word))

def create_hashset(path):
    hashset = set()

    with open(path, 'r') as file:
        for line in file:
            word = linha.strip()
            hashset.add(palavra)

    return hashset





