from datetime import datetime

a = '2024-05-29T00:00:00Z'  # or '2024-05-29'

# List comprehension to parse and format a single date
formatted_date = [datetime.strptime(a, '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d') if 'T' in a else datetime.strptime(a, '%Y-%m-%d').strftime('%Y-%m-%d')][0]

# Print the formatted date
print(formatted_date)


