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
rsa_private_exponent = rsa_sender.create_private_exponent(rsa_public_key[1])

challenges = [
  {
    'name': 'Caesar Cipher',
    'description': 'The Caesar Cipher shifts all letters forward in the alphabet a fixed number of places.',
    'encode': lambda text: encryption.encode_caesar_cipher(text, caesar_offset),
    'decode': lambda text: encryption.decode_caesar_cipher(text, caesar_offset),
    'plaintext': 'Welcome to the Teaching Security Administration Cryptography League!',
    'hint': f'Here, all letters are shifted forward {caesar_offset} places in the alphabet.'
  },
  {
    'name': 'Vigenere Cipher',
    'description': f'The Vigenere Cipher is like a better version of the Caesar Cipher, where each letter is shifted by a different amount. Here, the key is "{vigenere_key}."',
    'encode': lambda text: encryption.encode_vigenere_cipher(text, vigenere_key),
    'decode': lambda text: encryption.decode_vigenere_cipher(text, vigenere_key),
    'plaintext': 'Vigenere cipher!',
    'hint': f'The word "hello" encrypted with a key of "dog" becomes "{encryption.encode_vigenere_cipher("hello", "dog")}."'
  },
  {
    'name': 'Polybius Square',
    'description': 'The Polybius Square cipher is a substitution cipher encoded using a grid of letters. I and J are encoded the same way.',
    'encode': lambda text: encryption.encode_polybius_cipher(text),
    'decode': lambda text: encryption.decode_polybius_cipher(text),
    'plaintext': 'Polybius Square is cool!',
    'hint': 'This table is used to encode the Polybius cipher: <table class="bordered-cells" style="line-height: 1.5rem;"><tr><th></th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th></tr><tr><th>1</th><td>A</td><td>B</td><td>C</td><td>D</td><td>E</td></tr><tr><th>2</th><td>F</td><td>G</td><td>H</td><td>I/J</td><td>K</td></tr><tr><th>3</th><td>L</td><td>M</td><td>N</td><td>O</td><td>P</td></tr><tr><th>4</th><td>Q</td><td>R</td><td>S</td><td>T</td><td>U</td></tr><tr><th>5</th><td>V</td><td>W</td><td>X</td><td>Y</td><td>Z</td></tr></table>'
  },
  {
    'name': 'Hash (LCG)',
    'description': f'This hash is based off of the linear congruential generator (LCG), a pseudorandom number generation algorithm. Pseudorandom number generators produce seemingly-random numbers based on a starting number (seed). Here is the process for encoding this hash:<br><br>1. Encode the message in A1Z26. That is, A = 01, B = 02, etc. For example, "hello" becomes "0805121215."<br>2. Feed this encoded number through {lcg_iterations} loops of the LCG formula, r_{{n + 1}} = a * r_{{n}} + c (mod m), where a, c, and m are constants.<br><br>By this algorithm, which word gets encoded to the encrypted message below? (Hint: the answer somewhere on this page.) Here are the values of a, c, and m used in the below encryption:<br><table><tr><td>a</td><td>{lcg_a}</td></tr><tr><td>c</td><td>{lcg_c}</td></tr><tr><td>m</td><td>{lcg_m}</td></tr></table>',
    'encode': lambda text: encryption.encode_lcg_message(text, lcg_a, lcg_c, lcg_m, lcg_iterations),
    'decode': None, # This is not a reversible algorithm!
    'plaintext': 'process',
    'hint': 'It is not easy to reverse this algorithm. Try using brute force.'
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
