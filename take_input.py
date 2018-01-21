input("Press Enter to continue...")

temp = 0
try:
    while True:
        print(temp)
        temp = temp + 1
except KeyboardInterrupt:
    print("the final number is ")
    print(temp)
    pass
