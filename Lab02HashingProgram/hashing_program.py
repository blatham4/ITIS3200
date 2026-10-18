import hashlib 
import json
import os


def hash_file(filepath):
    #Creates a hash object SHA-256. 
    #Concept of the hash library and open file learned through brainstorming with AI. 
    sha256 = hashlib.sha256()

    #opens file in bianry read mode and iterates until all data is read. 
    with open(filepath, "rb") as file:
        while True:
            data = file.read(4096)

            if not data:
                break
            #adds data to hash
            sha256.update(data)
    #returns hash through hexadecimal
    return sha256.hexdigest()


def traverse_directory(directory):
    files = []
    # Goes through the directory and all of its subdirectories.
    for root, directories, filenames in os.walk(directory):
        for filename in filenames:

             # Creates the full path to the file. 
             #Concept learned and studied using AI help. 
            filepath = os.path.join(root, filename)

             # Creates a hash for the file.
            file_hash = hash_file(filepath)

            #adds file path and hash to the list. 
            files.append({
                "filepath": filepath,
                "hash": file_hash
            })

    return files


def generate_table(directory):

    #gathers all files and their hashes
    #transverse_directory was knowledge from AI that I studied and learned. 
    files = traverse_directory(directory)
    #creates and saves the file in .json format. 
    with open("hash_table.json", "w") as file:
        json.dump(files, file, indent=4)

    print("Hash table generated")


def validate_hash(directory):
    #checks if the hash table exists, if not returns it does not and ends. 
    if not os.path.exists("hash_table.json"):
        print("Hash table does not exist.")
        return

    #opens hash table and loads json information
    with open("hash_table.json", "r") as file:
        stored_files = json.load(file)

    #gets current file and creates new hashes
    current_files = traverse_directory(directory)
    #created to store old hashes
    stored_dictionary = {}

    #goes through saved files and stores filepath and old hash. 
    for file in stored_files:
        stored_dictionary[file["filepath"]] = file["hash"]
    
    current_dictionary = {}
    #goes through files and stores filepath and hash
    for file in current_files:
        current_dictionary[file["filepath"]] = file["hash"]

    #checks all files from original hash table. 
    for filepath in stored_dictionary:
        #if original file is not found it says file deleted. 
        if filepath not in current_dictionary:
            print("File deleted:", filepath)
        #if original file is found it says it is valid. 
        elif stored_dictionary[filepath] == current_dictionary[filepath]:
            print(filepath, "hash is valid")
        #a different hash so the file was changed. 
        else:
            print(filepath, "hash is invalid")
    #checks all current files. If not in original hash table it says new file detected. 
    for filepath in current_dictionary:

        if filepath not in stored_dictionary:
            print("New file detected:", filepath)


def main():
    #keeps going until user decides to exit 
    while True:

        
        print("       Hashing Program")
        print("1. Generate new hash table")
        print("2. Verify hashes")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":

            directory = input("Enter directory path: ")
            #asks user for a directory if it exists, if not then it creates a hash table. 
            if os.path.isdir(directory):
                generate_table(directory)
            #If it doesnt exits it just prints does not exist. 
            else:
                print("Directory does not exist.")

        elif choice == "2":
            #asks for directory
            directory = input("Enter directory path: ")
            #if it exists it verifies the file
            if os.path.isdir(directory):
                validate_hash(directory)
            #if it does not exist it prints to the user. 
            else:
                print("Directory does not exist.")

        elif choice == "3":
            #user is exiting so it prints goodbye and stops loop
            print("Goodbye!")
            break
        #any other option is invalid only 1-3
        else:

            print("Invalid choice.")

# Checks if this file is being run directly and starts the main. 
if __name__ == "__main__":
    main()