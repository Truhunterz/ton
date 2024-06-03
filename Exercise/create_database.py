import os

def save_parcel_details(length, width, height, weight, price, filename="parcel_details.txt"):
    current_directory = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(current_directory, filename)
    
    try:
        with open(filepath, 'a') as file:  # Open file in append mode
            file.write(f"Length: {length} cm\n")
            file.write(f"Width: {width} cm\n")
            file.write(f"Height: {height} cm\n")
            file.write(f"Weight: {weight} kg\n")
            file.write(f"Price: ${int(price)} \n \n")
        print(f"Parcel details appended to {filepath}")
    except IOError as e:
        print(f"An error occurred while saving the file: {e}")
