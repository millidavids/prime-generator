import random
import math
import time

# Lambda for generating a random odd binary array of length n
rba = lambda n: [1] + [random.randrange(2) for i in range(1,n - 1)] + [1]

# Strip leading zeros from a binary array
def stripLeadingZeros(x):
  while (len(x) > 0 and x[len(x) - 1] == 0):
    del x[len(x) - 1]
  return x

# Binary addition algorithm
def binAdd(x, y):
  if (len(x) > len(y)):
    for n in range(len(x) - len(y)):
      y += [0]
  else:
    for n in range(len(y) - len(x)):
      x += [0]
  a = [0 for i in range(0, len(x))]
  c = 0
  for i in range(0, len(x)):
    if (c == 1):
      if (x[i] == y[i]):
        if (x[i] == 1):
          a[i] = 1
        else:
          a[i] = 1
          c = 0
      else:
        a[i] = 0
    else:
      if (x[i] == y[i]):
        if (x[i] == 1):
          a[i] = 0
          c = 1
        else:
          a[i] = 0
      else:
        a[i] = 1
  if (c == 1):
    a += [1]
  return stripLeadingZeros(a)

# Binary subtraction algorithm, assume x > y
def binSubtract(x, y):
  if (len(x) > len(y)):
    for n in range(len(x) - len(y)):
      y += [0]
  d = [0 for i in range(0, len(x))]
  c = 0
  for i in range(0, len(x)):
    if (c == 1):
      if (x[i] == y[i]):
        if (x[i] == 1):
          d[i] = 1
        else:
          d[i] = 1
      else:
        d[i] = 0
      if (y[i] == d[i]):
        if (y[i] == 0):
          c = 0
    else:
      if (x[i] == y[i]):
        if (x[i] == 1):
          d[i] = 0
        else:
          d[i] = 0
      else:
        d[i] = 1
      if (y[i] == d[i]):
        if (y[i] == 1):
          c = 1
  return stripLeadingZeros(d)

# Binary multiplication algorithm
def binMultiply(x, y):
  z = []
  for i in range(len(y) -1, -1, -1):
    z = binAdd(z, z)
    if y[i] == 1:
      z = binAdd(z, x)
  return z

# Binary division algorithm, assume x > y
def binDivide(x, y):
  q = []
  r = []
  for i in range(len(x) - 1, -1, -1):
    q = binAdd(q, q)
    r = binAdd(r, r)
    if (x[i] == 1):
      r = binAdd(r, [1])
    if (binGreater(r, y) == r or binGreater(r, y) == []):
      r = binSubtract(r, y)
      q = binAdd(q, [1])
  return stripLeadingZeros(q), stripLeadingZeros(r)

# Compares two bin arrays and returns the greatest or an empty array
def binGreater(x ,y):
  while (len(x) > 0 and x[len(x) - 1] == 0):
    del x[len(x) - 1]
  while (len(y) > 0 and y[len(y) - 1] == 0):
    del y[len(y) - 1]
  if (len(x) > len(y)):
    for n in range(len(x) - len(y)):
      y += [0]
  else:
    for n in range(len(y) - len(x)):
      x += [0]
  for i in range(len(x) - 1, -1, -1):
    if (x[i] > y[i]):
      return stripLeadingZeros(x)
    if (y[i] > x[i]):
      return stripLeadingZeros(y)
  return []

# Modulus addition on two binary arrays
def modBinAdd(x, y, n):
  while (len(n) > 0 and n[len(n) - 1] == 0):
    del n[len(n) - 1]
  a = binAdd(x, y)
  while(len(a) > len(n)):
    a = binSubtract(a, n)
    stripLeadingZeros(n)
  if (binGreater(a, n) == []):
    return []
  if (binGreater(a, n) == a):
    return binSubtract(a, n)
  else:
    return stripLeadingZeros(a)

# Modulus multiplication on two binary arrays
def modBinMultiply(x, y, n):
  a = binMultiply(x, y)
  if (binGreater(a, n) == a):
    q, r = binDivide(a, n)
    return r
  else:
    return a

# Modulus exponentiation x raised to the y modulus n
def modBinExponentiation(x, y, n):
  z = [1]
  for i in range(len(y) - 1, -1, -1):
    z = modBinMultiply(z, z, n)
    if y[i] == 1:
      z = modBinMultiply(z, x, n)
  return z

# Primality test algorithm
def primalityTest(x):
  if (modBinExponentiation([1,0,1], binSubtract(x, [1]), x) == [1]):
    return True
  else:
    return False

# Brute force primality test using all divisors up to the number's square root
def bruteForcePrimalityTest(x):
  root = int(math.floor(math.sqrt(x)))
  for i in range(2, root + 1):
    if (x % i == 0):
      return False
  return True

# This runs if the file is called explicitly with `python hmwk5.py`
if __name__ == '__main__':
  print("\n----- Generating 100 Primes -----")
  sixteen_bit_primes = []
  while(len(sixteen_bit_primes) < 100):
    pot_prime = rba(16)
    forwards_pot_prime = int(str(''.join(str(x) for x in reversed(pot_prime))))
    decimal_pot_prime = int(str(''.join(str(x) for x in reversed(pot_prime))), 2)
    result = primalityTest(pot_prime)
    if result:
      sixteen_bit_primes.append([pot_prime, forwards_pot_prime, decimal_pot_prime])

  print("\n----- Brute Force 16-Bit Prime Test -----")
  error_count = 0
  for i in range(len(sixteen_bit_primes)):
    if (not bruteForcePrimalityTest(sixteen_bit_primes[i][2])):
      error_count += 1
  print('Error count: ' + str(error_count))

  print("\n----- Count Before Finding Prime -----")
  count_before_16_bit_prime = 0
  pot_prime_16 = rba(16)
  start_time = time.time()
  while(not primalityTest(pot_prime_16)):
    count_before_16_bit_prime += 1
    pot_prime_16 = rba(16)
  time_taken = time.time() - start_time
  print('16-bit: ' + ' Count: ' + str(count_before_16_bit_prime) + 
        ' :: Time Taken(seconds): ' + str(time_taken) +
        ' :: Binary: ' + str(''.join(str(x) for x in reversed(pot_prime_16))) +
        ' :: Decimal: ' + 
        str(int(str(''.join(str(x) for x in reversed(pot_prime_16))), 2)))

  count_before_32_bit_prime = 0
  pot_prime_32 = rba(32)
  start_time = time.time()
  while(not primalityTest(pot_prime_32)):
    count_before_32_bit_prime += 1
    pot_prime_32 = rba(32)
  time_taken = time.time() - start_time
  print('32-bit: ' + ' Count: ' + str(count_before_32_bit_prime) + 
        ' :: Time Taken(seconds): ' + str(time_taken) +
        ' :: Binary: ' + str(''.join(str(x) for x in reversed(pot_prime_32))) +
        ' :: Decimal: ' + 
        str(int(str(''.join(str(x) for x in reversed(pot_prime_32))), 2)))

  count_before_64_bit_prime = 0
  pot_prime_64 = rba(64)
  start_time = time.time()
  while(not primalityTest(pot_prime_64)):
    count_before_64_bit_prime += 1
    pot_prime_64 = rba(64)
  time_taken = time.time() - start_time
  print('64-bit: ' + ' Count: ' + str(count_before_64_bit_prime) + 
        ' :: Time Taken(seconds): ' + str(time_taken) +
        ' :: Binary: ' + str(''.join(str(x) for x in reversed(pot_prime_64))) +
        ' :: Decimal: ' + 
        str(int(str(''.join(str(x) for x in reversed(pot_prime_64))), 2)))

  count_before_128_bit_prime = 0
  pot_prime_128 = rba(128)
  start_time = time.time()
  while(not primalityTest(pot_prime_128)):
    count_before_128_bit_prime += 1
    pot_prime_128 = rba(128)
  time_taken = time.time() - start_time
  print('128-bit: ' + ' Count: ' + str(count_before_128_bit_prime) + 
        ' :: Time Taken(seconds): ' + str(time_taken) +
        ' :: Binary: ' + str(''.join(str(x) for x in reversed(pot_prime_128))) +
        ' :: Decimal: ' + 
        str(int(str(''.join(str(x) for x in reversed(pot_prime_128))), 2)))

  print("\n----- Average Count and Time -----")
  bits = [16, 32, 64, 128]
  for b in range(0, len(bits)):
    total_time = 0
    total_count = 0
    for i in range(0, 20):
      count_before_prime = 0
      pot_prime = rba(bits[b])
      start_time = time.time()
      while(not primalityTest(pot_prime)):
        total_count += 1
        pot_prime = rba(bits[b])
      total_time += time.time() - start_time
    print(str(bits[b]) + '-bit: ' + ' Average Count: ' + str(total_count/20.0) + 
          ' :: Average Time Taken(seconds): ' + str(total_time/20.0))

