#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import re

MAPPING = {
    'പ്രവർത്തനം': 'def',
    'അക്കം': '',
    'പാട്യം': '',
    'സത്യമായ്': 'True',
    'അസത്യമായ്': 'False',
    'ആവർത്തനം': 'for',
    'തവണ': 'in range',
    'തിരികെകൊടുക്കുക': 'return',
    'എങ്കിൽ': 'if',
    'ഇല്ലെങ്കിൽ': 'else',
    'പരിശോധിക്കുക': 'if',
    'പ്രദർശിപ്പിക്കുക': 'print',
}

def manjari_to_python(manjari_code):
    # Normalize line endings to \n
    manjari_code = manjari_code.replace('\r\n', '\n')
    
    lines = manjari_code.split('\n')
    python_lines = []
    
    for line in lines:
        if not line.strip():
            python_lines.append('')
            continue
        
        # Process the line by stripping it and then translating
        stripped_line = line.strip()
        
        # Calculate original indentation level (number of leading spaces)
        indent_level = len(line) - len(line.lstrip())
        
        # Apply translations to the stripped line
        translated_line = stripped_line
        for mal, py in MAPPING.items():
            translated_line = translated_line.replace(mal, py)
        
        # Add proper indentation back
        if indent_level > 0:
            python_lines.append(' ' * indent_level + translated_line)
        else:
            python_lines.append(translated_line)
    
    # Post-process the code to fix indentation issues
    fixed_code = '\n'.join(python_lines)
    
    # Fix specific indentation issue with non-indented lines that have leading spaces
    fixed_lines = []
    for line in fixed_code.split('\n'):
        # Top-level lines should have no indentation at all
        if not line.startswith('    ') and line.strip() and not any(line.lstrip().startswith(kw) for kw in ['if ', 'else:', 'elif ', 'except ', 'finally:']):
            fixed_lines.append(line.lstrip())  # Remove any leading spaces
        else:
            fixed_lines.append(line)
    
    return '\n'.join(fixed_lines)

def run_manjari_code(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            manjari_code = f.read()

        python_code = manjari_to_python(manjari_code)

        # Execute the Python code
        exec(python_code, {})
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("ഉപയോഗം: manjari <ഫയൽപേര്>")
        sys.exit(1)

    file_path = sys.argv[1]
    run_manjari_code(file_path)
