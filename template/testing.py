import uuid
# Define the file path
file_path = 'nginx-config-template'
path = str(uuid.uuid4())
# Define the dictionary with old strings as keys and new strings as values
replacements = {
    'GEN_PATH': path,
    'DOCKER_URL': 'http://testing:123/',
}

# Open the file, read its contents, replace the strings, and save the file
with open(file_path, 'r') as file:
    content = file.read()

# Replace each old string with its corresponding new string
for old_string, new_string in replacements.items():
    content = content.replace(old_string, new_string)

# Write the updated content back to the file

with open(path, 'w') as file:
    file.write(content)

print(f"Replaced multiple strings in {file_path}")

