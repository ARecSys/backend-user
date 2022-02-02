import jwt
import os
key="os.environ['SECRET_KEY']"
payload={'public_id': "user.public_id", 'exp' : 34435523}
token = jwt.encode(payload, key)
print (token)
decoded = jwt.decode(token, key) # works in PyJWT >= v2.0
print (decoded)