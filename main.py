from flask import Flask, request, render_template_string, send_file
import itertools
import os

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

def vigenere_decrypt(ciphertext, key):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    key = key.lower()
    decrypted_text = []
    key_length = len(key)
    
    for i, char in enumerate(ciphertext.lower()):
        if char in alphabet:
            key_char = key[i % key_length]
            shifted_index = (alphabet.index(char) - alphabet.index(key_char)) % 26
            decrypted_text.append(alphabet[shifted_index])
        else:
            decrypted_text.append(char)
            
    return ''.join(decrypted_text)

def brute_force_vigenere(ciphertext):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    possible_decryptions = []
    
    for key_tuple in itertools.product(alphabet, repeat=3):
        key = ''.join(key_tuple)
        decrypted_word = vigenere_decrypt(ciphertext, key)
        possible_decryptions.append((key, decrypted_word))
    
    return possible_decryptions

def format_decryptions(possible_decryptions):
    found_words = []
    other_words = []

    for key_or_shift, word in possible_decryptions:
        if word in hashset:
            found_words.append((key_or_shift, word))
        else:
            other_words.append((key_or_shift, word))

    prioritized_decryptions = found_words + other_words
    result = "<div style='margin-top: 20px;'>"
    for key_or_shift, word in prioritized_decryptions:
        color = "green" if word in hashset else "black"
        result += f"<h4 style=\"color:{color}; margin: 5px;\"> Key: {key_or_shift}, Word: {word} </h4>"
    result += "</div>"

    return result

def save_to_file(filename, possible_decryptions):
    with open(filename, 'w') as file:
        for key_or_shift, word in possible_decryptions:
            file.write(f"Key: {key_or_shift}, Word: {word}\n")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        uploaded_file = request.files['file']
        if uploaded_file and uploaded_file.filename.endswith('.txt'):
            content = uploaded_file.read().decode('utf-8')
            first_line = content.splitlines()[0]
            cipher_type = request.form['cipher']
            
            if cipher_type == 'caesar':
                result = brute_caesar(first_line)
                filename = 'caesar_output.txt'
            elif cipher_type == 'vigenere':
                result = brute_force_vigenere(first_line)
                filename = 'vigenere_output.txt'
            
            save_to_file(filename, result)
            
            return render_template_string('''
                <html>
                    <head>
                        <title>Cifra de César e Vigenère - Brute Force</title>
                        <style>
                            body {
                                font-family: Arial, sans-serif;
                                background-color: #f4f4f4;
                                color: #333;
                                margin: 0;
                                padding: 20px;
                            }
                            h1 {
                                color: #007BFF;
                            }
                            .container {
                                max-width: 600px;
                                margin: 0 auto;
                                background: white;
                                padding: 20px;
                                border-radius: 8px;
                                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                            }
                            input[type="file"] {
                                margin-bottom: 10px;
                            }
                            input[type="submit"] {
                                padding: 10px 15px;
                                background-color: #007BFF;
                                color: white;
                                border: none;
                                border-radius: 5px;
                                cursor: pointer;
                            }
                            input[type="submit"]:hover {
                                background-color: #0056b3;
                            }
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <h1>Cifra de César e Vigenère Brute Force</h1>
                            <form method="post" enctype="multipart/form-data">
                                <input type="file" name="file" accept=".txt" required>
                                <br>
                                <input type="radio" name="cipher" value="caesar" checked> Cifra de César
                                <input type="radio" name="cipher" value="vigenere"> Cifra de Vigenère
                                <br>
                                <input type="submit" value="Enviar">
                            </form>
                            <hr>
                            <h2>Resultados:</h2>
                            <div>{{ results|safe }}</div>
                            <hr>
                            <a href="/download/{{ filename }}" download="{{ filename }}">Download Resultados</a>
                        </div>
                    </body>
                </html>
            ''', results=format_decryptions(result), filename=filename)
    
    return render_template_string('''
        <html>
            <head>
                <title>Cifra de César e Vigenère - Brute Force</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        background-color: #f4f4f4;
                        color: #333;
                        margin: 0;
                        padding: 20px;
                    }
                    h1 {
                        color: #007BFF;
                    }
                    .container {
                        max-width: 600px;
                        margin: 0 auto;
                        background: white;
                        padding: 20px;
                        border-radius: 8px;
                        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                    }
                    input[type="file"] {
                        margin-bottom: 10px;
                    }
                    input[type="submit"] {
                        padding: 10px 15px;
                        background-color: #007BFF;
                        color: white;
                        border: none;
                        border-radius: 5px;
                        cursor: pointer;
                    }
                    input[type="submit"]:hover {
                        background-color: #0056b3;
                    }
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Cifra de César e Vigenère Brute Force</h1>
                    <form method="post" enctype="multipart/form-data">
                        <input type="file" name="file" accept=".txt" required>
                        <br>
                        <input type="radio" name="cipher" value="caesar" checked> Cifra de César
                        <input type="radio" name="cipher" value="vigenere"> Cifra de Vigenère
                        <br>
                        <input type="submit" value="Enviar">
                    </form>
                </div>
            </body>
        </html>
    ''')

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)
