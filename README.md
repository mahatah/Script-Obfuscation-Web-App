## Script Obfuscation Web App

This Flask web application provides a convenient interface for obfuscating scripts by converting string literals into their ASCII representations. Originally designed for PowerShell script obfuscation, it can handle any file type where strings are wrapped in single or double quotes.

### Features
- **File Upload**: Users can upload their script files directly through the web interface.
- **String Obfuscation**: The application processes the uploaded file, identifying and obfuscating all string literals.
- **Download Processed File**: The obfuscated script file is made available for download.

### How It Works
1. **Upload Script**: Users upload their script files through the provided form.
2. **Obfuscation Process**: The backend processes the file, converting all string literals to obfuscated ASCII representations.
3. **Download Obfuscated Script**: Users can download the processed file, which is ready for secure use.

### Technologies Used
- **Flask**: For the web framework.
- **HTML/CSS**: For the frontend design.
- **Python**: For processing and obfuscating the script files.

### How to Run and Use `app.py`

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/mahatah/Script-Obfuscation-Web-App.git
   cd Script-Obfuscation-Web-App
   ```

2. **Set Up a Virtual Environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```bash
   python app.py
   ```
   The application will start running on `http://127.0.0.1:5000/`.

5. **Access the Web Interface**:
   Open your web browser and navigate to `http://127.0.0.1:5000/` to access the application.

### Changing the Port

To change the port the application runs on, you can modify the last line of `app.py`:

```python
if __name__ == '__main__':
    app.run(debug=True, port=5000)  # Change the port number here
```

Replace `5000` with your desired port number.

### Directory Structure
Ensure your project directory is structured as follows:

```
your_project_directory/
│
├── app.py
├── requirements.txt
├── static/
│   └── images/
│       └── obfuscate.png
├── templates/
│   └── index.html
├── uploads/
└── downloads/
```

### Short Description
This Flask web app obfuscates script files by converting string literals into their ASCII representations. Upload your script, and the app processes it to obfuscate all string literals. Originally designed for PowerShell, it supports any file type with quoted strings. Download the obfuscated script easily.
