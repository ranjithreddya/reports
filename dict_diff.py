# Define the two lists a and b
a = [
    {"name": "John Doe", "age": 30, "email": "johndoe1@example.com"},
    {"name": "John Doe", "age": 30, "email": "johndoe2@example.com"},
    {"name": "John Doe", "age": 30, "email": "johndoe3@example.com"}
]

b = [
    {"name": "John Doe", "age": 30, "email": "johndoe1@example.com"},
    {"name": "John Doe", "age": 30, "email": "johndoe2@example.com"}
]

# Identify elements in list a that are not in list b, and vice versa
not_in_b = [item for item in a if item not in b]
not_in_a = [item for item in b if item not in a]

print(f"Items in 'a' but not in 'b': {not_in_b}")
print(f"Items in 'b' but not in 'a': {not_in_a}")
