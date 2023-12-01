from cmu_graphics import *
import json

print(str(rgb(125, 125, 125)))

class MyClass:
    def __init__(self, name):
        self.name = name
        self.dustyBlue = rgb(116, 136, 168)
        self.mossGreen = rgb(89, 125, 92)
        self.sand = rgb(247, 246, 228)
    
    def to_json(self):
        return {
            'name': self.name,
            'dustyBlue': self.dustyBlue,
            'mossGreen': self.mossGreen,
            'sand': self.sand
        }
        
def set_default(obj):
    try:
        if isinstance(obj, set):
            return list(obj)
        elif isinstance(obj, str):
            return obj
        elif isinstance(obj, list):
            return obj
        else: 
            return str(obj)
    except:
        print("an error occurred")


# rgb and hex conversion functions were taken from GeeksForGeeks link above
def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb

# Create an instance of the class
# cellDict = {0: "0. Go", 1: "1. oops", 2: "2. weapon", 3: "3. secret, owner is None", 4: "4. secret, owner is None"}

cellSet = {1, 2, 3}

obj = MyClass('colors')

# Convert the object to a JSON string
json_str = json.dumps(obj.to_json(), default=set_default)

# Print the JSON string
print(json_str)