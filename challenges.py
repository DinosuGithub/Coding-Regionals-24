import encryption # See encryption.py

caesar_offset = 18
vigenere_key = 'cryptography'

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
    'hint': 'Take a look at this table: <h1>test</h1> [replace this]'
  },
]
