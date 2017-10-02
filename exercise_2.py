def searching_traffic(list_of_cars):# Separating the list into 4 lists with 6 items per list and finding the biggest item
    result = []
    tup1 = ('4:00pm', max(list_of_cars[:6]))
    result.append(tup1)
    tup2 = ('5:00pm', max(list_of_cars[6:12]))
    result.append(tup2)
    tup3 = ('6:00pm', max(list_of_cars[12:18]))
    result.append(tup3)
    tup4 = ('7:00pm', max(list_of_cars[18:24]))
    result.append(tup4)
    return result


def count_list(list_of): # Counting the list if it has 24 items
    while len(list_of) != 24:
        print("\nThe list should consist of 24 items")
        list_of = eval(input("Give the list of cars again: "))
        list_of = check_list(list_of)
    return list_of


def check_list(list_of): # Checking if the user's input is a list
    while type(list_of) is not list:
        print("\nYour input should be a list ")
        print("For example: [23,24,34,45,43,23,57,34,65,12,19,45,54,65,54,43,89,48,42,55,22,69,23,93]")
        list_of = eval(input("Give the list of cars: "))
    return list_of


if __name__ == '__main__':
    list_of_cars = []
    while True: # Checking generally if the user's input is valid
        try:
            list_of_cars = eval(input("Give the list of cars: "))
            break
        except:
            print("Your input is not valid")
            print("Your input should be like: [23,24,34,45,43,23,57,34,65,12,19,45,54,65,54,43,89,48,42,55,22,69,23,93]\n")
    list_of_cars = check_list(list_of_cars)
    list_of_cars = count_list(list_of_cars)
    pr_result = searching_traffic(list_of_cars)
    print(pr_result)