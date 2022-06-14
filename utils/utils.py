import datetime as dt
import random
import string

def time_now(fmt='%Y-%m-%d-%H%M%S'):
  now = dt.datetime.utcnow()
  return now.strftime(fmt)

def gen_random(length):
  print(''.join(random.choices(string.digits + string.ascii_lowercase, k=length)))