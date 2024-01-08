#importing the packages needed
import random
import requests

#connecting with API I will use - "The Cat API" - breeds and pictures
breeds_API_url = "https://api.thecatapi.com/v1/breeds"
image_API_url = "https://api.thecatapi.com/v1/images/search"

#using the API key (it is free and given after signing in on the website)
API_key = "live_v6Ape8V1YmMS8fEXZGgKnPWoQe8yBuLdrPWdCiymxKzqq9cSCOkeq2fUgYEHXYc9"

#getting the breeds from the API
def get_cat_breeds():
    try:
        #defining the headers with the API key
        headers = {"x-api-key": API_key}
        response = requests.get(breeds_API_url, headers=headers)

# I am making sure everthing works. That the API responded (200 = request worked)
        if response.status_code == 200:
            breeds_data = response.json()
            return breeds_data
# in case of errors this is what the program should do. The first is if there is an error in the data request and the second concerning network problems
        else:
            print("There was an error retrieving breed data from the API. Check your connection.")
            return []
    except requests.exceptions.RequestException:
        print("An error ocurred. There might be network problems.")
        return []

#getting the images from the API
def get_breed_image(breed_id):
    try:
        #defining headers and using the API key
        headers = {"x-api-key": API_key}
        params = {"breed_ids": breed_id}
        response = requests.get(image_API_url, headers=headers, params=params)

        if response.status_code == 200:
            image_data = response.json()
            if image_data and len(image_data) > 0:
                return image_data[0].get("url", "")
            else:
                return None
# in case of errors this is what the program should do. The first is if there is an error in the data request and the second concerning network problems
        else:
            print("There was an error retrieving image data from the API. Check your connection.")
            return None
    except requests.exceptions.RequestException:
        print("An error ocurred in image loading. There might be network problems.")
        return None

# Creating the main entry point (or the main program with which the user will interact)
if __name__ == "__main__":
    # Asking for the user's name and creating a welcoming message
    user_name = input("Miau, Human! Are you sure you want to enter our kingdom? 😈 What should we call you, slave? \n").title()
    print("Welcome,", user_name, "to our Cat Universe!")
    cat_breeds_list = get_cat_breeds()

    if cat_breeds_list:
        #printing the list of cat breeds
        print("Types of Cats in the world:")
        for i, breed in enumerate(cat_breeds_list, start=1):
            print(f"{i}. {breed['name']}")

        while True:
            try:
                #interacting with the user to ask which breed number it wants
                user_choice = int(input("Which Cat interests you? Enter at your own risk. Choose a number from 1 to " + str(len(cat_breeds_list)) + " (enter '0' for a random cat or '100' to leave):\n"))
                goodbye_message = ("Hasta la Vista, Kitty 🐈 (or the name you use in your human world: " + user_name + ")!")
                #creating a random breed choice
                if user_choice == 0:
                    user_choice = random.randint(1, len(cat_breeds_list))
                if user_choice == 100:
                    print(goodbye_message)
                    break

                if 1 <= user_choice <= len(cat_breeds_list) != 100:
                    selected_breed = cat_breeds_list[user_choice - 1]
                    breed_id = selected_breed["id"]

                    #slicing the description - give only 50 characters.
                    cat_description = selected_breed["description"]
                    description_summary = cat_description[:100] + ("..." if len(cat_description) > 100 else "")

                    # summing up the major cat information in a variable
                    cat_summed_info = f"""
                        Information for the magestic: {selected_breed["name"]}
                        Summed description: {description_summary}
                        Temperament: {selected_breed["temperament"]}
                        Origin: {selected_breed["origin"]}
                        Life Span: {selected_breed["life_span"]}
                        Adaptability (from 0-5): {selected_breed["adaptability"]}
                        Affection Level (from 0-5): {selected_breed["affection_level"]}
                        Hypoallergenic: {"Yes" if selected_breed["hypoallergenic"] else "No"}
                        Wikipedia URL (click to visit the webpage): {selected_breed["wikipedia_url"]}
                        """

                    print(cat_summed_info)
                    # writing the results of user choser
                    with open("cat_results.txt", "a+") as file:
                        file.write(cat_summed_info)
                        file.write("\n\n")
                    print("We saved your search history into a new file 🔎 Don't worry we are just collecting intel about you, humans!")

                    # Getting the breed image URL
                    breed_image_url = get_breed_image(breed_id)
                    if breed_image_url:
                        print("Take a look at the Breed you choose. Here is the link:", breed_image_url)
                    else:
                        print("I'm sorry. This breed is quite shy, so we don't have any photo to show you.")
                    #giving more options to user: to get to know more or to see the list of breeds again
                    more_info_option = input("Do you want to delve in this breed and get more information? (yes/no) \n").lower()
                    if more_info_option != "yes":
                        show_list_option = input("Want to see the list of breeds again? (yes/no) \n".lower())

                        if show_list_option == "yes":
                            print("Types of Cats in the world:")
                            for i, breed in enumerate(cat_breeds_list, start=1):
                                print(f"{i}. {breed['name']}")
                            continue
                        else:
                            print(goodbye_message)
                            break
                    #defining what is showned if the user wants more information
                    else:
                        cat_more_info = f"""
                            Here are some more facts about (from 0-5): {selected_breed["name"]}
                            Full description: {selected_breed["description"]}
                            Child Friendly: {selected_breed["child_friendly"]}
                            Dog Friendly: {selected_breed["dog_friendly"]}
                            Energy Level: {selected_breed["energy_level"]}
                            Grooming: {selected_breed["grooming"]}
                            Health Issues: {selected_breed["health_issues"]}
                            Intelligence: {selected_breed["intelligence"]}
                            Shedding Level: {selected_breed["shedding_level"]}
                            Social Needs: {selected_breed["social_needs"]}
                            Stranger Friendly: {selected_breed["stranger_friendly"]}
                            Vocalisation: {selected_breed["vocalisation"]}
                        """
                        print(cat_more_info)

                        print("Types of Cats in the world:")
                        for i, breed in enumerate(cat_breeds_list, start=1):
                            print(f"{i}. {breed['name']}")
                        continue

             #print messages in case there is an error on the users input
                else:
                    print("Miau Miau Miau... 🤔 Invalid choice! You have to select a valid breed number!")
            except ValueError:
                print("Miau Miau Miau... 🤔 You have to select a valid breed number!")

