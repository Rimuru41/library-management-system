import bcrypt
password="kamal"
hashed_password=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
print(hashed_password)
hashed=bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())
print(hashed)


print('$2b$12$bq3avPM3BLATPQWwh/CWNOR90JhgrqETEQgM7/qhwUlAHExeA4Aqy')
