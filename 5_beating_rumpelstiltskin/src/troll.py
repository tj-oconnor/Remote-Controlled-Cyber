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
print(" 1. His favorite number equals the product of a * b ")
print(" 2. b is less than c*e+d-c-a")
print(" 3. c * 20 equals the product of d * c * f")
print(" 4. d/f equals c")
print(" 5. e equals the product of d * d * c")
print(" 6. f equals c - a")
print(" 7. c equals (b - 1)/e")
print(" 8. a,b,c,d,e,f and his favorite number are all greater than 0")
print(" 9. a,b,c,d,e,f and his favorite number are all less than 9999")
print("-------------------------------------------------------------")
guessed = int(input("What is Rumpelstiltskin's favorite number? >>> "))

print("Sleeping 10 seconds to prevent brute force attacks. ")
time.sleep(10)

if guessed == 7503:
    print("\n<<< That's it!  You guessed his favorite number.")
else:
    print("\n<<< Sorry, try again.")
