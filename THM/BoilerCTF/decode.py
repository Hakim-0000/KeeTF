import base64

hash_values = [int(x) for x in "079 084 108 105 077 068 089 050 077 071 078 107 079 084 086 104 090 071 086 104 077 122 073 051 089 122 085 048 077 084 103 121 089 109 070 104 078 084 069 049 079 068 081 075".split()]

hashed_string = ''.join(chr(val) for val in hash_values)

encoded_string = "OTliMDY2MGNkOTVhZGVhMzI3YzU0MTgyYmFhNTE1ODQK"
decoded_bytes = base64.b64decode(encoded_string)
decoded_string = decoded_bytes.decode('utf-8')

print(decoded_string)

