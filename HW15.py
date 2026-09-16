def shutdown():
    
    user_input = input("Do you want to shut down? (Yes/No): ")
    
    if user_input == "Yes":
        print("shutting down")
    elif user_input == "no":
        print("abort shut down")
    else:
        print("sorry")

shutdown()
