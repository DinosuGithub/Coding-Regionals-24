alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

# Substitution ciphers

# Function to handle encoding/decoding for substitution ciphers
def handle_cipher(text, key, char_algorithm, char_length=1, non_punctuation=alphabet):
  uppercase = text.upper()
  if isinstance(key, str):
    key = key.upper()

  result = ''

  encountered_letters = 0
  new_chars = ''
  for char in uppercase:
    if char in non_punctuation:
      if encountered_letters % char_length == 0:
        new_chars = ''

      new_chars += char
      
      if encountered_letters % char_length == char_length - 1:
        result += char_algorithm(new_chars, key, encountered_letters)

      encountered_letters += 1
    else:
      result += char

  return result

def encode_caesar_char(char, offset, encountered_letters):
  return alphabet[(alphabet.index(char.upper()) + offset) % len(alphabet)]

def decode_caesar_char(char, offset, encountered_letters):
  return alphabet[(alphabet.index(char) - offset) % len(alphabet)]

def encode_vigenere_char(char, key, encountered_letters):
  key_char = key[encountered_letters % len(key)]
  offset = alphabet.index(key_char)
  return alphabet[(alphabet.index(char) + offset) % len(alphabet)]

def decode_vigenere_char(char, key, encountered_letters):
  key_char = key[encountered_letters % len(key)]
  offset = alphabet.index(key_char)
  return alphabet[(alphabet.index(char) - offset) % len(alphabet)]

def encode_polybius_char(char, key, encountered_letters):
  alphabet_index = alphabet.index(char)
  if alphabet_index > alphabet.index('I'):
    alphabet_index -= 1
  
  return str(alphabet_index // 5 + 1) + str(alphabet_index % 5 + 1)

def decode_polybius_char(chars, key, encountered_letters):
  alphabet_ind = 5*(int(chars[0]) - 1) + int(chars[1]) - 1
  if alphabet_ind > alphabet.index('I'):
    alphabet_ind += 1
  
  return alphabet[alphabet_ind]


def encode_caesar_cipher(text, offset):
  return handle_cipher(text, offset, encode_caesar_char)

def decode_caesar_cipher(text, offset):
  return handle_cipher(text, offset, decode_caesar_char)

def encode_vigenere_cipher(text, key):
  return handle_cipher(text, key, encode_vigenere_char)

def decode_vigenere_cipher(text, key):
  return handle_cipher(text, key, decode_vigenere_char)

def encode_polybius_cipher(text):
  return handle_cipher(text, None, encode_polybius_char)

def decode_polybius_cipher(text):
  return handle_cipher(text, None, decode_polybius_char, 2, list('12345'))


# Non-substitution ciphers

class RSAExchange:
  def __init__(self, p, q):
    self.p = p
    self.q = q
    self.totient = (p - 1) * (q - 1)

  # Euclidean Algorithm
  @staticmethod
  def get_gcd(a, b):
    if a < b:
      a, b = b, a
    
    while True:
      remainder = a % b
      if remainder == 0:
        return b
  
      a, b = b, remainder

  def generate_public_keys(self):
    keys = []
    
    for key in range(2, self.totient):
      if self.get_gcd(key, self.totient) == 1:
        keys.append(key)
  
    return keys

  # Modification of Extended Euclidean Algorithm
  def create_private_key(self, public_key):
    k = 1
    while True:
      if (k * self.totient + 1) % public_key == 0:
        return (k * self.totient + 1) // public_key

      k += 1

a = RSAExchange(11, 13)
p = a.generate_public_keys()
print(p[0])
print(a.create_private_key(p[0]))