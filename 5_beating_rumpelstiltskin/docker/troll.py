import time

print("-------------------------------------------------------------")
print(" Troll Constraint Solver v 0x31337")
print("-------------------------------------------------------------")
print("Hey you!  I hear you're trying to escape the forest. That")
print("Rumpelstiltskin sure can be a pain. Ever since that queen")
print("figured out his name, he's had to come up with a new riddle.")
print("Well, today's your lucky day. I happen to know his favorite")
print("number.  I can't just tell you what it is, but if you guess,")
print("I'll tell you whether you got. it right.\n")
print("-------------------------------------------------------------")
print(" Here is what I know about his favorite number: ")
print("  1. His favorite number * 123 equals a" )
print("  2. b is equal to a - 6 " )
print("  3. c equals b plus a " )
print("  4. d equals a plus b plus c ") 
print("  5. d equals 3691464 " )
print("  6. His favorite number is > 0 and < 9999 ") 
print("-------------------------------------------------------------")

foo = int(input("What is Rumpelstiltskin's favorite number? >>> "))

print("Sleeping 10 seconds to prevent brute force attacks. ")
time.sleep(10)

if foo == 7503:
    print("\n<<< That's it!  You guessed his favorite number.")
    print("\n<<< Since you like games so much - cd /usr/games")
else:
    print("\n<<< Sorry, try again.")
