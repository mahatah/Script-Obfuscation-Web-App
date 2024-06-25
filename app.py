from flask import Flask, request, send_from_directory, render_template
import os
import re
import logging

# 2024 Mahatah (https://victim.site). All rights reserved.

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['DOWNLOAD_FOLDER'] = 'downloads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['DOWNLOAD_FOLDER'], exist_ok=True)

# Setup logging
logging.basicConfig(level=logging.INFO)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        logging.error("No file part in the request")
        return "No file part", 400
    
    file = request.files['file']
    if file.filename == '':
        logging.error("No selected file")
        return "No selected file", 400
    
    if file:
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        output_path = os.path.join(app.config['DOWNLOAD_FOLDER'], file.filename)
        file.save(input_path)
        try:
            obfuscate_script(input_path, output_path)
            logging.info(f"File processed successfully: {file.filename}")
            return send_from_directory(app.config['DOWNLOAD_FOLDER'], file.filename)
        except Exception as e:
            logging.error(f"Error processing file {file.filename}: {str(e)}")
            return f"Error processing file: {str(e)}", 500
        finally:
            # Cleanup uploaded file
            try:
                os.remove(input_path)
            except Exception as e:
                logging.warning(f"Failed to delete uploaded file {input_path}: {str(e)}")

def obfuscate_script(input_path, output_path):
    try:
        with open(input_path, 'r') as file:
            content = file.read()
    except Exception as e:
        raise Exception(f"Error reading input file: {str(e)}")

    # Regex pattern to match string literals
    pattern = re.compile(r'(?<!`)\"([^\"]*?)(?<!`)\"|\'([^\']*?)(?<!\')\'', re.MULTILINE)
    matches = pattern.finditer(content)

    for match in matches:
        original_string = match.group(0)
        extracted_string = match.group(1) or match.group(2)
        if extracted_string:
            converted_string = convert_to_ascii_index_string(extracted_string, wrap_with_to_string=True)
            content = content.replace(original_string, converted_string, 1)  # Ensure each replacement happens only once

    try:
        with open(output_path, 'w') as file:
            file.write(content)
    except Exception as e:
        raise Exception(f"Error writing to output file: {str(e)}")

def convert_to_ascii_index_string(input_string, wrap_with_to_string=False):
    char_string_index_array = ''.join(f"[char]{ord(char)} + " for char in input_string).rstrip(' + ')
    if wrap_with_to_string:
        char_string_index_array = f"({char_string_index_array}).ToString()"
    return char_string_index_array

if __name__ == '__main__':
    app.run(debug=True)
