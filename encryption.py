alphabet = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

phonetic_alphabet = 'Alfa, Bravo, Charlie, Delta, Echo, Foxtrot, Golf, Hotel, India, Juliett, Kilo, Lima, Mike, November, Oscar, Papa, Quebec, Romeo, Sierra, Tango, Uniform, Victor, Whiskey, X-ray, Yankee, Zulu'.split(', ')


def normalize(text, allowed_chars=alphabet + [' ']):
  text = text.upper()
  
  normalized = ''
  for char in text:
    if char in allowed_chars:
      normalized += char

  return normalized

def check_answer(response, answer):
  return normalize(response) == normalize(answer)  

# Substitution ciphers

# Function to handle encoding/decoding for substitution ciphers
def handle_cipher(text, key, char_algorithm, char_length=1, non_punctuation=alphabet, encode_separator='', decode_separator=''):
  uppercase = text.upper()
  
  if isinstance(key, str):
    key = key.upper()

  result = ''
  
  encountered_letters = 0
  new_chars = ''

  non_punctuation_count = [char in non_punctuation for char in uppercase].count(True) // char_length # Number of non-punctuation characters in text

  handled_chars = 0
  
  for char_i, char in enumerate(uppercase):
    if char in non_punctuation:
      if encountered_letters % char_length == 0:
        new_chars = ''

      new_chars += char
      
      if encountered_letters % char_length == char_length - 1:
        handled_chars += 1
        result += char_algorithm(new_chars, key, encountered_letters)
        if handled_chars != non_punctuation_count:
          result += encode_separator

      encountered_letters += 1
    elif encode_separator == '' and char != decode_separator:
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

def encode_a1z26_char(char, key, encountered_letters):
  return str(alphabet.index(char) + 1).rjust(2, '0')

def decode_a1z26_char(chars, key, encountered_letters):
  return alphabet[int(chars) - 1]

def encode_affine_char(char, key, encountered_letters):
  return alphabet[(alphabet.index(char) * key[0] + key[1]) % len(alphabet)]

def decode_affine_char(char, key, encountered_letters):
  # Find modular multiplicative inverse
  multiplicative_inverse = 1
  while (key[0] * multiplicative_inverse) % len(alphabet) != 1:
    multiplicative_inverse += 1

  # Solve
  return alphabet[multiplicative_inverse * (alphabet.index(char) - key[1]) % len(alphabet)]

def encode_spelling_alphabet_char(char, key, encountered_letters):
  return phonetic_alphabet[alphabet.index(char)]


def encode_caesar_cipher(text, offset):
  return handle_cipher(text, offset, encode_caesar_char)

def decode_caesar_cipher(text, offset):
  return handle_cipher(text, offset, decode_caesar_char)

def encode_vigenere_cipher(text, key):
  return handle_cipher(text, key, encode_vigenere_char)

def decode_vigenere_cipher(text, key):
  return handle_cipher(text, key, decode_vigenere_char)

def encode_polybius_cipher(text):
  return handle_cipher(text, None, encode_polybius_char, 1, alphabet, ' ')

def decode_polybius_cipher(text):
  return handle_cipher(text, None, decode_polybius_char, 2, list('12345'), '', ' ')

def encode_a1z26(text):
  return handle_cipher(text, None, encode_a1z26_char, 1, alphabet, ' ')

def decode_a1z26(text):
  return handle_cipher(text, None, decode_a1z26_char, 2, list('0123456789'), '', ' ')

def encode_affine_cipher(text, slope, intercept):
  return handle_cipher(text, (slope, intercept), encode_affine_char)

def decode_affine_cipher(text, slope, intercept):
  return handle_cipher(text, (slope, intercept), decode_affine_char)

def encode_spelling_alphabet(text):
  return handle_cipher(text, None, encode_spelling_alphabet_char, 1, alphabet, encode_separator=' ')

def decode_spelling_alphabet(text):
  return ''.join([letter[0].upper() for letter in text.split(' ')])


# Non-substitution ciphers

# Message to concatenated A1Z26
def message_to_int(message):
  return int(handle_cipher(message, None, encode_a1z26_char, 1, alphabet).replace(' ', ''))

# Concatenated A1Z26 to message
def int_to_message(integer):
  encoded = str(integer)
  if len(encoded) % 2 == 1:
    encoded = '0' + encoded
  
  return handle_cipher(encoded, None, decode_a1z26_char, 2, list('0123456789'))


def generate_lcg_random(seed, a, c, m):
  return (a * seed + c) % m

def encode_lcg_message(text, a, c, m, iterations):
  message_int = message_to_int(text)
  
  for _ in range(iterations):
    message_int = generate_lcg_random(message_int, a, c, m)

  return message_int


class RSASender:
  def __init__(self, p, q):
    self.p = p
    self.q = q
    self.public_modulus = p * q
    self.totient = (p - 1) * (q - 1)

    self.private_exponent = None

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

  def public_exponent_options(self):
    keys = []
    
    for key in range(2, self.totient):
      if self.get_gcd(key, self.totient) == 1:
        keys.append(key)
  
    return keys

  def create_public_key(self, public_exponent):
    return (self.public_modulus, public_exponent)

  # Modification of Extended Euclidean Algorithm
  def create_private_exponent(self, public_exponent):
    k = 1
    while True:
      if (k * self.totient + 1) % public_exponent == 0:
        key = (k * self.totient + 1) // public_exponent
        self.private_exponent = key
        return key

      k += 1

  def decode_message(self, message):
    return (message ** self.private_exponent) % self.public_modulus

# Parameter public_key is of the form (modulus, exponent)
def encode_rsa_message(message, public_key):
  int_message = message_to_int(message)
  return (int_message ** public_key[1]) % public_key[0]

def decode_rsa_message(message, sender):
  return int_to_message(sender.decode_message(int(message)))


def char_to_binary(char):
  ascii_value = ord(char)
  binary_value = ''

  for i in range(8):
    power = 2 ** (7 - i)
    new_digit = ascii_value // power
    binary_value += str(new_digit)
    ascii_value -= new_digit * power

  return binary_value

def binary_to_char(binary):
  ascii_value = 0

  for digit_i, digit in enumerate(binary):
    ascii_value += int(digit) * 2 ** (7 - digit_i)

  return chr(ascii_value)

def encode_binary(text):
  return ' '.join([char_to_binary(char) for char in text])

def decode_binary(text):
  return ''.join([binary_to_char(char) for char in text.split(' ')])
