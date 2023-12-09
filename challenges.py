import encryption # See encryption.py

caesar_offset = 18
vigenere_key = 'cryptography'

rsa_sender = encryption.RSASender(397, 587)
rsa_public_exponent = rsa_sender.public_exponent_options()[100]
rsa_public_key = rsa_sender.create_public_key(rsa_public_exponent)
rsa_private_exponent = rsa_sender.create_private_exponent(rsa_public_key[1])


challenges = [
  {
    'name': 'Caesar Cipher',
    'description': 'Solve Caesar.',
    'encode': lambda text: encryption.encode_caesar_cipher(text, caesar_offset),
    'decode': lambda text: encryption.decode_caesar_cipher(text, caesar_offset),
    'plaintext': 'Hello world!',
    'hint': f'All letters are shifted forward {caesar_offset} places in the alphabet.'
  },
  {
    'name': 'Vigenere Cipher',
    'description': 'Solve this Vigenere problem!',
    'encode': lambda text: encryption.encode_vigenere_cipher(text, vigenere_key),
    'decode': lambda text: encryption.decode_vigenere_cipher(text, vigenere_key),
    'plaintext': 'Vigenere',
    'hint': '[Insert good hint]'
  },
  {
    'name': 'Polybius Square',
    'description': 'Solve the Polybius square',
    'encode': lambda text: encryption.encode_polybius_cipher(text),
    'decode': lambda text: encryption.decode_polybius_cipher(text),
    'plaintext': 'Polybius',
    'hint': 'Take a look at this table: <table class="bordered-cells" style="line-height: 2rem;"><tr><th></th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th></tr><tr><th>1</th><td>A</td><td>B</td><td>C</td><td>D</td><td>E</td></tr><tr><th>2</th><td>F</td><td>G</td><td>H</td><td>I/J</td><td>K</td></tr><tr><th>3</th><td>L</td><td>M</td><td>N</td><td>O</td><td>P</td></tr><tr><th>4</th><td>Q</td><td>R</td><td>S</td><td>T</td><td>U</td></tr><tr><th>5</th><td>V</td><td>W</td><td>X</td><td>Y</td><td>Z</td></tr></table>'
  },
  {
    'name': 'RSA',
    'description': f'The commander of the administration has sent you an urgent message encrypted with RSA. Use your RSA information to read his instructions. When you have the message in number form, decode it using A1Z26 (ex. 0809 = "hi"). Hint: use <a href="https://www.wolframalpha.com/" target="_blank">Wolfram Alpha</a> for large math computations.<table><tr><td>Private exponent:</td><td>{rsa_private_exponent}</td></tr><tr></tr><tr><td>Public modulus:</td><td>{rsa_public_key[0]}</td></tr><td>Public exponent:</td><td>{rsa_public_key[1]}</td></table>',
    'encode': lambda text: encryption.encode_rsa_message(text, rsa_public_key),
    'decode': lambda text: encryption.int_to_message(rsa_sender.decode_integer_message(int(text))),
    'plaintext': 'run',
    'hint': 'From the table, the only information you need is your private exponent and public modulus.'
  },
]
