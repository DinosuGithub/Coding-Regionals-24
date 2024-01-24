from flask import url_for
import encryption # See encryption.py

caesar_offset = 18

vigenere_key = 'cryptography'

lcg_a = 4359287924442956
lcg_c = 147458333
lcg_m = 4503599627370449
lcg_iterations = 10

rsa_sender = encryption.RSASender(397, 587)
rsa_public_exponent = rsa_sender.public_exponent_options()[100]
rsa_public_key = rsa_sender.create_public_key(rsa_public_exponent)
rsa_private_exponent = rsa_sender.create_private_exponent(rsa_public_exponent)

affine_slope = 11
affine_intercept = 6

challenges = [
  {
    'name': 'Caesar Cipher',
    'description': 'Here is a simple challenge to start you off. The Caesar Cipher shifts all letters forward a fixed number of places in the alphabet. Figure out what this shift amount is for the encrypted message below, and use it to decode the answer.',
    'encode': lambda text: encryption.encode_caesar_cipher(text, caesar_offset),
    'decode': lambda text: encryption.decode_caesar_cipher(text, caesar_offset),
    'plaintext': 'Welcome to the Teaching Security Administration Cryptography League!',
    'hint': f'Here, all letters are shifted forward {caesar_offset} places in the alphabet.'
  },
  {
    'name': 'Vigenere Cipher',
    'description': f'The Vigenere Cipher is like applying a different Caesar Cipher encryption to every character. That is, each letter is shifted by a different amount, determined by a different letter in the key. Here, the key is "{vigenere_key}."',
    'encode': lambda text: encryption.encode_vigenere_cipher(text, vigenere_key),
    'decode': lambda text: encryption.decode_vigenere_cipher(text, vigenere_key),
    'plaintext': 'Though Giovan Battista Bellaso originally invented the cipher, it was named after Blaise de Vigenere.',
    'hint': f'The word "hello" encrypted with a key of "dog" becomes "{encryption.encode_vigenere_cipher("hello", "dog")}."'
  },
  {
    'name': 'Polybius Square',
    'description': 'The Polybius Square cipher is a substitution cipher encoded using a 5x5 grid of letters. I and J are encoded the same way. Determine how this encoding works, and use it to decode the encrypted message. Note that spaces are not encoded, so letters are separated by spaces in the ciphertext.',
    'encode': lambda text: encryption.encode_polybius_cipher(text),
    'decode': lambda text: encryption.decode_polybius_cipher(text),
    'plaintext': 'The next cipher will be much more modern.',
    'hint': 'This table is used to encode the Polybius cipher: <table class="bordered-cells" style="line-height: 1.5rem;"><tr><th></th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th></tr><tr><th>1</th><td>A</td><td>B</td><td>C</td><td>D</td><td>E</td></tr><tr><th>2</th><td>F</td><td>G</td><td>H</td><td>I/J</td><td>K</td></tr><tr><th>3</th><td>L</td><td>M</td><td>N</td><td>O</td><td>P</td></tr><tr><th>4</th><td>Q</td><td>R</td><td>S</td><td>T</td><td>U</td></tr><tr><th>5</th><td>V</td><td>W</td><td>X</td><td>Y</td><td>Z</td></tr></table>'
  },
  {
    'name': 'Hash (LCG)',
    'description': f'This hash is based off of the linear congruential generator (LCG), a pseudorandom number generation algorithm. Pseudorandom number generators produce seemingly-random numbers based on a starting number (seed). Here is the process for encoding this hash:<br><ol><li>Encode the message in <a href="/challenge/7">A1Z26</a>. That is, A = 01, B = 02, etc. For example, "hello" becomes "0805121215."</li><li>Feed this encoded number through {lcg_iterations} loops of the LCG formula, r<sub>n + 1</sub> = a * r<sub>n</sub> + c (mod m), where a, c, and m are constants.</li></ol>By this algorithm, which word gets encoded to the encrypted message below? (Hint: the word is somewhere on this page.) Here are the values of a, c, and m used in the below encryption:<br><table><tr><td>a</td><td>{lcg_a}</td></tr><tr><td>c</td><td>{lcg_c}</td></tr><tr><td>m</td><td>{lcg_m}</td></tr></table>',
    'encode': lambda text: encryption.encode_lcg_message(text, lcg_a, lcg_c, lcg_m, lcg_iterations),
    'decode': None, # This is not a reversible algorithm!
    'plaintext': 'process',
    'hint': 'It is not easy to reverse this algorithm. Try using brute force (checking every possible answer), since you know the answer is one of the words above. Remember that incorrect entries are recorded and make your score worse!'
  },
  {
    'name': 'RSA',
    'description': f'The commander of the administration has sent you an urgent message encrypted with RSA. Use your private and public RSA information below to read his instructions. When you have the message in number form, decode it using <a href="/challenge/7">A1Z26</a> (ex. 0809 = "hi"). Hint: use <a href="https://www.wolframalpha.com/" target="_blank">Wolfram Alpha</a> for large math computations.<table><tr><td>Private exponent:</td><td>{rsa_private_exponent}</td></tr><tr></tr><tr><td>Public modulus:</td><td>{rsa_public_key[0]}</td></tr><td>Public exponent:</td><td>{rsa_public_key[1]}</td></table>',
    'encode': lambda text: encryption.encode_rsa_message(text, rsa_public_key),
    'decode': lambda text: encryption.decode_rsa_message(text, rsa_sender),
    'plaintext': 'run',
    'hint': 'From the table, the only information you need is your private exponent and public modulus.'
  },
  {
    'name': 'Binary',
    'description': 'In binary encoding, each character is encoded into a binary (base 2) string of length 8. The binary value of each character is determined by converting its ASCII value from base 10 to binary.',
    'encode': lambda text: encryption.encode_binary(text),
    'decode': lambda text: encryption.decode_binary(text),
    'plaintext': 'Did that make you feel like a hacker?',
    'hint': 'In this encoding, capitalization matters, and punctuation is encoded like any other character.'
  },
  {
    'name': 'A1Z26',
    'description': f'In A1Z26 encoding, each letter is encoded to its position in the alphabet. For example, "hello" becomes "{encryption.encode_a1z26("hello")}."',
    'encode': lambda text: encryption.encode_a1z26(text),
    'decode': lambda text: encryption.decode_a1z26(text),
    'plaintext': 'This cipher is not very secure.',
    'hint': 'Spaces are not encoded, so letters are separated by spaces in the ciphertext.'
  },
  {
    'name': 'Affine Cipher',
    'description': f'The Affine Cipher uses a linear function to transform each letter in the plaintext. A letter in the plaintext is encoded with this process:<ol><li>Let x be the position in the alphabet of an input letter</li><li>Let y = mx + b, where m and b define the key of the cipher</li><li>The encoded letter is the letter at position y of the alphabet</li></ol>Here are the values of m and b used in the encryption below:<table><tr><td>m</td><td>{affine_slope}</td></tr><tr><td>b</td><td>{affine_intercept}</td></tr></table>',
    'encode': lambda text: encryption.encode_affine_cipher(text, affine_slope, affine_intercept),
    'decode': lambda text: encryption.decode_affine_cipher(text, affine_slope, affine_intercept),
    'plaintext': 'In this cipher, the value of m has to be coprime with the length of the alphabet.',
    'hint': 'Do not use division to decode a letter. In modular arithmetic, one multiplicative inverse of x (mod 26) is the number n that you can multiply x by such that nx is 1 more than a multiple of 26.'
  },
  {
    'name': 'Spelling Alphabet',
    'description': f'One use of the spelling alphabet is to clearly communicate words between people who are talking over a shaky phone line. Figure out the message encrypted in the text below.',
    'encode': lambda text: encryption.encode_spelling_alphabet(text),
    'decode': lambda text: encryption.decode_spelling_alphabet(text),
    'plaintext': 'Nice work! Or should I say, "bravo!"',
    'hint': 'This cipher is not very complicated! Observe how some words appear many times.'
  }
]
