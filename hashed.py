import bcrypt
password="kamal"
hashed_password=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
print(hashed_password)
print(bcrypt.checkpw(password.encode('utf-8'), hashed_password))
