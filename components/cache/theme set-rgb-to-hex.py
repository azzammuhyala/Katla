import json

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def convert_colors(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, list) and len(value) == 3 and all(isinstance(i, int) for i in value):
                data[key] = rgb_to_hex(value)
            else:
                convert_colors(value)

    elif isinstance(data, list):
        for item in data:
            convert_colors(item)

def main():
    with open('themes.json', 'r') as file:
        data = json.load(file)

    convert_colors(data)

    with open('themes-converted.json', 'w') as file:
        json.dump(data, file, indent=4)

if __name__ == '__main__':
    main()