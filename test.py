import sys
import re
import requests
import json
replay_file_path = 'D:/Documents/Code/Slippi-Ranked-Tool/replays/ranked-inprogress.slp'
#handlers = {ParseEvent.METADATA: print}
# handlers = {ParseEvent.START: print}
# parse(sys.stdin.buffer, handlers)
# Open the binary file in read mode

# Read hexadecimal data from stdin
hex_data = sys.stdin.buffer.read()

# # Remove any spaces or newline characters from the input
# hex_data = hex_data.decode('utf-8').replace(" ", "").replace("\n", "").encode('utf-8')
# print(hex_data[588:617])
raw_codes = hex_data[588:617]
full_width_marker = b'\x81\x94'

text_parts = []
i = 0

while i < len(raw_codes):
    # Check if the current byte is the full-width marker
    if raw_codes[i:i+2] == full_width_marker:
        # Full-width character (2 bytes)
        text_parts.append(raw_codes[i:i+2].decode('shift-jis'))
        i += 2
    else:
        # Half-width character (1 byte)
        text_parts.append(raw_codes[i:i+1].decode('shift-jis'))
        i += 1

joint = ''.join(text_parts)
opp_code = re.sub(r'DF＃950|\s+', '', joint).replace("\x00", "").replace("＃", "#")
print(opp_code)


url = "https://gql-gateway-dot-slippi.uc.r.appspot.com/graphql"

payload = f'{{"query":"fragment profileFields on NetplayProfile {{\\n  ratingOrdinal\\n}}\\n\\nfragment userProfilePage on User {{\\n  rankedNetplayProfile {{\\n    ...profileFields\\n  }}\\n}}\\n\\nquery AccountManagementPageQuery($cc: String!) {{\\n  getConnectCode(code: $cc) {{\\n    user {{\\n      ...userProfilePage\\n    }}\\n  }}\\n}}\\n",\"variables\":{{\"cc\":\"{opp_code}\"}}}}'
headers = {
  'Content-Type': 'application/json'
}
response = requests.request("POST", url, headers=headers, data=payload)

# print(response.text)
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    
    # Extract the value and round to the nearest tenth
    rating_ordinal = data["data"]["getConnectCode"]["user"]["rankedNetplayProfile"]["ratingOrdinal"]
    rounded_rating = round(rating_ordinal, 1)
    
    print(f"Rating: {rounded_rating}")
else:
    print(f"Request failed with status code: {response.status_code}")