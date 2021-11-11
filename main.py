from user_based_recom import user_based_recommendation
from item_based_recom import item_based_recommendations

path_selection = input("Please select option \n"
                       "[1]. User based recommendation based on Pearson \n"
                       "[2]. Item based recommendation \n")

if path_selection == "1":
    user_based_recommendation()

if path_selection == "2":
    item_based_recommendations()
