### Script Obfuscation Web App

This Flask web application provides a convenient interface for obfuscating scripts by converting string literals into their ASCII representations. Originally designed for PowerShell script obfuscation, it can handle any file type where strings are wrapped in single or double quotes.

#### Features:
- **File Upload**: Users can upload their script files directly through the web interface.
- **String Obfuscation**: The application processes the uploaded file, identifying and obfuscating all string literals.
- **Download Processed File**: The obfuscated script file is made available for download.
- **Hacker-Themed UI**: The web interface features a hacker-themed design to enhance user experience.

#### How It Works:
1. **Upload Script**: Users upload their script files through the provided form.
2. **Obfuscation Process**: The backend processes the file, converting all string literals to obfuscated ASCII representations.
3. **Download Obfuscated Script**: Users can download the processed file, which is ready for secure use.

#### Technologies Used:
- **Flask**: For the web framework.
- **HTML/CSS**: For the frontend design.
- **Python**: For processing and obfuscating the script files.

This tool is perfect for developers looking to add a layer of obfuscation to their scripts, making it harder for unauthorized users to read and understand the code.
