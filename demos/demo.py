# Sample data from your table
data = [
    {'order_no': '250327122930407233', 'user_id': 1005058036},
    {'order_no': '250327105621405247', 'user_id': 1005056349},
    {'order_no': '250327161316411120', 'user_id': 1005061476},
    {'order_no': '250327093710403941', 'user_id': 1005055622},
    {'order_no': '250326173031401244', 'user_id': 3005052527},
    {'order_no': '250326160730399269', 'user_id': 3004947579},
    {'order_no': '250326175632401703', 'user_id': 1005052748},
    {'order_no': '250327132229407975', 'user_id': 3005058869},
    {'order_no': '250327171421412328', 'user_id': 1005062634},
    {'order_no': '250327131548407884', 'user_id': 3005058802}
]

# Calculate user_id mod 30 for each entry
for row in data:
    row['user_id_mod_30'] = row['user_id'] % 30

# Print the results in a formatted table
print("order_no           |  user_id    | user_id mod 30")
print("-------------------+-------------+---------------")
for row in data:
    print(f"{row['order_no']} | {row['user_id']:10d} | {row['user_id_mod_30']:13d}")