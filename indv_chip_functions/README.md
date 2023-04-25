Under this section, use the test files found in pico_test_files for a designated chip and correctly format them into a proper python function that can be implemented into main. For instance for a return function,

def add_numbers(num1, num2):
    """
    Adds two numbers together and returns the result.
    """
    result = num1 + num2
    return result

# Call the add_numbers function and pass in 5 and 7 as arguments
sum = add_numbers(5, 7)

# Print the result of the function call
print(sum)  # Output: 12

If you have a void function, 

def print_hello(name):
    """
    Prints a greeting message with the given name.
    """
    print("Hello, " + name + "!")

print_hello("Alice")
