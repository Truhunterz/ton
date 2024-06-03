def calculate_price(length, width, height, weight):
    volume = length * width * height
    if weight <= 1:
        if volume <= 5000:
            return 3
        elif volume <= 10000:
            return 5
        else:
            return 7
    elif weight <= 5:
        if volume <= 5000:
            return 5
        elif volume <= 10000:
            return 7
        else:
            return 9
    else:
        if volume <= 5000:
            return 7
        elif volume <= 10000:
            return 9
        else:
            return 11
