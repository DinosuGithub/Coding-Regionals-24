This is documentation for [encryption.py](/encryption.py)

# Encoding/Decoding Examples
Import the module:
``` python
import encryption
```

## Caesar Cipher
``` python
shift = 18
encoded = encryption.encode_caesar_cipher('my message', shift)
decoded = encryption.decode_caesar_cipher(encoded, shift)
```

## Vigenere Cipher
``` python
key = 'cryptography'
encoded = encryption.encode_vigenere_cipher('my message', key)
decoded = encryption.decode_vigenere_cipher(encoded, key)
```

## Polybius Square
``` python
encoded = encryption.encode_polybius_cipher('my message')
decoded = encryption.decode_polybius_cipher(encoded)
```

## LCG (Linear Congruential Generator) Hash
``` python
a = 4359287924442956
c = 147458333
m = 4503599627370449
iterations = 10 # Number of times to pass through generator
encoded = encryption.encode_lcg_message('my message', a, c, m, iterations)
# No decoding function because the hash is not reversible
```

## RSA
``` python
primes = (397, 587)
sender = encryption.RSASender(primes[0], primes[1])
public_exponent = sender.public_exponent_options()[100] # Of all possible public exponents, use the one at index 100 when sorted from least to greatest
public_key = sender.create_public_key(public_exponent)
private_exponent = sender.create_private_exponent(public_exponent)

encoded = encryption.encode_rsa_message('wow', public_key) # The concatenated A1Z26 form of the input must be less than the public modulus (public_key[0])
decoded = encryption.int_to_message(rsa_sender.decode_message(encoded))
```

## Binary
``` python
encoded = encryption.encode_binary('my message')
decoded = encryption.decode_binary(encoded)
```


# All Encryption Documentation*
*See above examples first. Most of the section below is not necessary to be understood by the module user.

## General functions:
* `normalize`: removes non-alphabet characters except space, converts to uppercase
* `check_answer`: checks if the normalized values of two inputs are equal

## Substitution ciphers*:
_*Note that using the full string functions calls other functions appropriately._

### General functions:
* `handle_cipher`: converts every group of `char_length` characters in a string to a different string with the function `char_algorithm`

### Character functions (ex. `encode_caesar_char`, `decode_polybius_char`, etc.):
* Each function returns output character(s) from input character(s)
* Passed into `handle_cipher` as `char_algorithm` parameter

### Full string functions (ex. `encode_caesar_cipher`, `decode_polybius_cipher`):
* Each function returns the encoded/decoded output of the entire input text

## Non-substitution ciphers:
## General functions:
* `message_to_int`: converts a message string to concatenated A1Z26 (ex. "ABCXYZ" = 010203242526)
* `int_to_message`: converts concatenated A1Z26 to a message string

## LCG (Linear Congruential Generator) Hash:
* `generate_lcg_random`: returns the output of an LCG with given seed and parameters
* `encode_lcg_message`: returns the output of feeding the concatenated A1Z26 of `text` through an LCG with specified parameters, `iterations` times

## RSA Encryption:
### `RSASender`:
* Generates private and public data for message receiver
* Takes in two primes
* `public_exponent_options`: gets all options for public exponents
* `create_public_key`: returns tuple of form `(<public modulus>, <public exponent>)`
* `create_private_exponent`: creates private exponent from public exponent using private totient
* `decode_integer_message`: decodes message in integer form

### `encode_rsa_message`:
* Generates message encrypted with receiver public key