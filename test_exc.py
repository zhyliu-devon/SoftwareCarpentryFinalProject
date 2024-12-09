def greet(name):
    print(f"Hello, {name}!")

print(1)

# Input text code
code_text = """
def run_custom_code():
    greet("World")  # Call the function from base_functions
    print("This is a dynamically executed code!")
run_custom_code()
"""
print(2)

# Execute the text as code, passing globals() to exec
exec(code_text, globals())
print(3)

# Dynamically defined function is now available
run_custom_code()
print(4)
