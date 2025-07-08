import random
subjects = ["Ali","Ahmed","Sara","Babar Azam","Mahira sharma","Ali Zafar","Group of monkeys",
            "Rickshaw Drivers"]
Actions = ["Launches","Dances with","Eats","Sings","Cancels","Declares war on","Orders",
           "Celebrates","Wishes"]
Places_Things = ["Quaid-e-Azam Mausoleum","Shahrah-e-faisal","Garden","Railway station",
                 "Court","Plate of samosa","Burger","Hat","Pen","Pencil"]
while True:
    subject = random.choice(subjects)
    action = random.choice(Actions)
    place_thing = random.choice(Places_Things)
    headline = f"Breaking News: {subject} {action} {place_thing}"
    print("\n"+headline)
    
    user_input = input("\nDo you want another headline?(Y/N)").strip().lower()
    #.strip() if user enters extra spaces so it will delete it
    # lower() converts to lower case
    if user_input == "n":
        break

print("\nThanks for using this fake headline generator")


