import json

def get_monthly_commission(deals, objective):
    total_commission = 0
    commissions = []
    current_total = 0
    objective_half = objective / 2

    for deal in deals:
        current_commission = 0
        if current_total + deal > objective_half:
            first_step_remaining = max(objective_half - current_total, 0)
            current_commission += first_step_remaining * 5 / 100
            if current_total <= objective_half:
                current_commission += (deal - first_step_remaining) * 10 / 100
            deal -= first_step_remaining
        else:
            current_commission += deal * 5 / 100
        if current_total + deal > objective:
            second_step_remaining = max(objective - current_total, 0)
            current_commission += second_step_remaining * 10 / 100
            current_commission += (deal - second_step_remaining) * 15 / 100
        current_total += deal
        total_commission += current_commission
        commissions.append(current_commission)
    return total_commission, commissions

def main():
    current_id = 1
    input_file = open('./data/input.json') # Open file
    output_file = open('./output.json', "w")

    data = json.load(input_file) # Load json content of file

    # Initialize result object
    result = {
        "commissions": [],
        "deals": []
    }

    users = {} # Create an empty array which will store total amount of sales by user

    # Initialize object with the right id's with an amount of 0
    for user in data["users"]:
        user_id = user["id"]
        users[user_id] = {"commissions": {}, "objective": user["objective"]}

    # Add amount to users by looping on the input file
    for deal in data["deals"]:
        corresponding_user = deal["user"]
        month = str(deal["payment_date"][:-3])
        amount = deal["amount"]
        if users[corresponding_user]["commissions"].has_key(month):
            users[corresponding_user]["commissions"][str(month)].append(amount)
        else:
            users[corresponding_user]["commissions"][str(month)] = [amount]

    print(json.dumps(users))

    for id_user in users:
        user_commissionnn = {
            "user_id" : id_user,
            "commission" : {}
        }
        print('aaa = ', users[id_user])
        for month in users[id_user]["commissions"]:
            month_deals = users[id_user]["commissions"][month]
            print("month_deals =", month_deals)
            print("month = ", month)
            commission, commissions = get_monthly_commission(month_deals, users[id_user]["objective"])
            user_commissionnn["commission"][month] = commission
            for one_commission in commissions:
                result["deals"].append(
                    {
                        "id" : current_id,
                        "commission" : one_commission
                    })
                current_id += 1
                # result_commission = {}
            print(commission)
            print(commissions)
        result["commissions"].append(user_commissionnn)
        print("\n\n")

    print(json.dumps(result))
    # Write the result in output_file
    output_file.write(json.dumps(result))

main()