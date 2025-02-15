from typing import Any, Optional
from smolagents.tools import Tool

class CodeRefactorTool(Tool):
    name = "code_refactor"
    description = "Analyzes and refactors code to improve its quality, readability and maintainability."
    inputs = {
         'code': {
            'type': 'string',
            'description': 'Source code to refactor'
        },
        'language': {
            'type': 'string',
            'description': 'Programming language',
            'default': 'python',
            'nullable': True
        }    }
    output_type = "string"

    def forward(self, code: str, language: str = "python") -> str:
        """
        Refactors the provided code according to best practices.
        
        Args:
            code: Source code to be refactored
            language: Programming language of the code (defaults to "python")
            
        Returns:
            Refactored code as a string
        """
        try:
            # Remove empty lines at start and end
            code = code.strip()
            
            if language.lower() == "python":
                # Basic Python code cleanup
                # Remove multiple blank lines
                code = "\n".join(line for line in code.splitlines() if line.strip())
                
                # Add docstring template if missing
                if not any(line.strip().startswith('"""') for line in code.splitlines()):
                    code = '"""Add docstring for this code.\n"""\n' + code
                
                # Ensure proper spacing around operators
                import re
                code = re.sub(r'([=\+\-\*/])', r' \1 ', code)
                
                # Add proper indentation
                lines = code.splitlines()
                indent_level = 0
                refactored_lines = []
                for line in lines:
                    if line.strip().endswith(':'):
                        refactored_lines.append('    ' * indent_level + line)
                        indent_level += 1
                    else:
                        refactored_lines.append('    ' * indent_level + line)
                code = '\n'.join(refactored_lines)
                
            return code

        except Exception as e:
            return f"Error during refactoring: {str(e)}\nOriginal code returned:\n{code}"

    def __init__(self, *args, **kwargs):
        self.is_initialized = False