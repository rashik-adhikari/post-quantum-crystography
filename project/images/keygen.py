#This is just a simple test to verify whether the algorithm is working or not
import main
import sys
import steg
# Step 1: Alice generates random keys and her public msg to Bob
alicePrivKey, aliceMsg = main.keygen()
print("Alice sends to Bob her public message:", aliceMsg)
