import json

input_file = open('./data/input.json') # Open file
output_file = open('./output.json', "w")

data = json.load(input_file) # Load json content of file

# Initialize result object
result = {
    "commissions": []
}

users = {} # Create an empty array which will store total amount of sales by user

# Initialize object with the right id's with an amount of 0
for user in data["users"]:
    user_id = user["id"]
    users[user_id] = []

# Add amount to users by looping on the input file
for deal in data["deals"]:
    corresponding_user = deal["user"]
    users[corresponding_user].append(deal["amount"])

for user in users:
    sales = users[user] # Get the list of sales
    total_sales = sum(sales)
    user_commission = 0
    # Add commission for each user with the corresponding conditions
    if total_sales > 2000:
        user_commission += 500
    if len(sales) > 2:
        user_commission += (total_sales * 20) / 100
    elif len(sales) > 0:
        user_commission += (total_sales * 10) / 100
    # Fill the object
    result["commissions"].append(
        {
            "user_id": user,
            "commission": user_commission,
        })

# Write the result in output_file
output_file.write(json.dumps(result))
