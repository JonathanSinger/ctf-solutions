#!/usr/bin/python
# CSAW2017 Quals - CVV
# @JonathanSinger
import socket
from random import Random
import copy
import re

"""
gencc: A simple program to generate credit card numbers that pass the
MOD 10 check (Luhn formula).
Usefull for testing e-commerce sites during development.
by ..:: crazyjunkie ::.. 2014
https://github.com/eye9poob/python/blob/master/credit-card-numbers-generator.py
"""

visaPrefixList = [
        ['4', '5', '3', '9'],
        ['4', '5', '5', '6'],
        ['4', '9', '1', '6'],
        ['4', '5', '3', '2'],
        ['4', '9', '2', '9'],
        ['4', '0', '2', '4', '0', '0', '7', '1'],
        ['4', '4', '8', '6'],
        ['4', '7', '1', '6'],
        ['4']]
mastercardPrefixList = [
        ['5', '1'],
        ['5', '2'],
        ['5', '3'],
        ['5', '4'],
        ['5', '5']]
amexPrefixList = [
        ['3', '4'],
        ['3', '7']]
discoverPrefixList = [
        ['6', '0', '1', '1']]

generator = Random()
generator.seed()

def luhn_checksum(card_number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(card_number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = 0
    checksum += sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d*2))
    return checksum % 10

def is_luhn_valid(card_number):
    return luhn_checksum(card_number) == 0

def completed_number(prefix, length):
    ccnumber = prefix

    while len(ccnumber) < (length - 1):
        digit = str(generator.choice(range(0, 10)))
        ccnumber.append(digit)

    sum = 0
    pos = 0

    reversedCCnumber = []
    reversedCCnumber.extend(ccnumber)
    reversedCCnumber.reverse()

    while pos < length - 1:
        odd = int(reversedCCnumber[pos]) * 2
        if odd > 9:
            odd -= 9
        sum += odd
        if pos != (length - 2):
            sum += int(reversedCCnumber[pos + 1])
        pos += 2

    checkdigit = ((sum / 10 + 1) * 10 - sum) % 10
    ccnumber.append(str(checkdigit))
    return ''.join(ccnumber)

def credit_card_number(rnd, prefixList, length, howMany):
    result = []

    while len(result) < howMany:
        ccnumber = copy.copy(rnd.choice(prefixList))
        result.append(completed_number(ccnumber, length))

    return result

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('misc.chal.csaw.io', 8308)
s.connect(server_address)

mode = 2

while True:
  data = s.recv(100)

  if 'flag' in data:
    print "[!] Received Flag: " + data.rstrip()
    break

  print "[-] Received Data: " + data.rstrip()

  if 'MasterCard' in data:
    print "[!] Found: MasterCard"
    number = credit_card_number(generator, mastercardPrefixList, 16, 1)[0]
  elif 'Visa' in data:
    print "[!] Found: Visa"
    number = credit_card_number(generator, visaPrefixList, 16, 1)[0]
  elif 'Discover' in data:
    print "[!] Found: Discover"
    number = credit_card_number(generator, discoverPrefixList, 16, 1)[0]
  elif 'American Express' in data:
    print "[!] Found: American Express"
    number = credit_card_number(generator, amexPrefixList, 15, 1)[0]
  elif 'starts with' in data:
    print "[!] Found: starts with"
    PrefixList = [re.findall('\d', data.rstrip())]
    number = credit_card_number(generator, PrefixList, 16, 1)[0]
  elif 'ends with' in data:
    print "[!] Found: ends with"
    endDigit = re.findall('\d', data.rstrip())
    endLength = len(endDigit)
    if endLength == 1:
      while True:
        number = credit_card_number(generator, visaPrefixList, 16, 1)[0]
        genLast = int(repr(int(number))[-1])
        if genLast == int(endDigit[0]): break
    elif endLength == 4:
      while True:
        number = credit_card_number(generator, visaPrefixList, 16, 1)[0]
        genLast = int(number) % 10000
        if str('%04d' % genLast) == ''.join(endDigit): break
  elif 'is valid' in data:
    print "[!] Found: is valid"
    checkMe = re.findall('\d', data.rstrip())
    del checkMe[-1]
    del checkMe[-1]
    if is_luhn_valid(''.join(checkMe)):
      number = '1'
      mode = 1
    else:
      number = '0'
      mode = 0

  print "[+] Sending: " + number

  s.sendall(number + "\n")

  if (mode == 1):
    data = s.recv(5)
  elif (mode == 0):
    data = s.recv(6)
  mode = 2

  data = s.recv(8)
  print "[-] Received Data: " + data.rstrip()

  if (data == ""): break

s.close()
