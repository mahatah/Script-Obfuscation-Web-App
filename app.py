from flask import Flask, request, send_from_directory, render_template, jsonify
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

def obfuscate_powershell_string(string):
    if(len(string) == 0) :
        return ""
    else:
        return '([char]' + ' + [char]'.join(str(ord(c)) for c in string) + ').ToString()'

def obfuscate_python_string(string):
    if(len(string) == 0) :
        return ""
    else:
        return '("".join([chr(' + '), chr('.join(str(ord(c)) for c in string) + ')]))'

def obfuscate_script(content, language):
    if language == 'PowerShell':
        pattern = r'(?<!`)\"([^\"]*?)(?<!`)\"|\'([^\']*?)(?<!\')\''
        obfuscate_func = obfuscate_powershell_string
    elif language == 'Python':
        pattern = r'(f?\".*?\"|f?\'.*?\')'
        obfuscate_func = obfuscate_python_string
    else:
        return content

    def replace_match(match):
        original_string = match.group(0)
        if original_string.startswith('f"') or original_string.startswith("f'"):
            extracted_string = original_string[2:-1]  # Remove f and surrounding quotes
            parts = re.split(r'(\{.*?\})', extracted_string)
            obfuscated_parts = [part if len(part) == 0 else obfuscate_func(part) + " + " if not part.startswith('{') else  "f\"" + part + "\" + " for part in parts]
            converted_string = "".join(obfuscated_parts)
            converted_string = converted_string[0:-3]
            return converted_string
        elif original_string.startswith('"') and original_string.endswith('"'):
            extracted_string = original_string[1:-1]
            converted_string = obfuscate_func(extracted_string)
            return f'{converted_string}'
        elif original_string.startswith("'") and original_string.endswith("'"):
            extracted_string = original_string[1:-1]
            converted_string = obfuscate_func(extracted_string)
            return f"{converted_string}"
        return original_string


    obfuscated_script = re.sub(pattern, replace_match, content)
    return obfuscated_script

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
            with open(input_path, 'r') as f:
                content = f.read()
            language = request.form.get('language', 'PowerShell')
            obfuscated_content = obfuscate_script(content, language)
            with open(output_path, 'w') as f:
                f.write(obfuscated_content)
            logging.info(f"File processed successfully: {file.filename}")
            return send_from_directory(app.config['DOWNLOAD_FOLDER'], file.filename)
        except Exception as e:
            logging.error(f"Error processing file {file.filename}: {str(e)}")
            return f"Error processing file: {str(e)}", 500
        finally:
            try:
                os.remove(input_path)
            except Exception as e:
                logging.warning(f"Failed to delete uploaded file {input_path}: {str(e)}")

@app.route('/obfuscate', methods=['POST'])
def obfuscate():
    data = request.get_json()
    script = data['script']
    language = data.get('language', 'PowerShell')
    obfuscated_script = obfuscate_script(script, language)
    return jsonify({'obfuscated_script': obfuscated_script})

if __name__ == '__main__':
    app.run(debug=True)
