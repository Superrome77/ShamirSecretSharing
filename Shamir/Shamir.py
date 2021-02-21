#Implementation of Shamir Secret Sharing Scheme 

import random 
from math import ceil 
from decimal import *
import tkinter as tk
from tkinter import *
window = tk.Tk()

#r.get_random_word()
#x = r.get_random_word()
global field_size 
global numberOfSharesRow
numberOfSharesRow = 0
field_size = 10**5
idList = ["a","b","c","d"]
entries = []
root = Tk()

def reconstructSecret(shares): 
	
	# Combines shares using 
	# Lagranges interpolation. 
	# Shares is an array of shares 
	# being combined 
	sums, prod_arr = 0, [] 
	
	for j in range(len(shares)): 
		xj, yj = shares[j][0],shares[j][1] 
		prod = Decimal(1) 
		
		for i in range(len(shares)): 
			xi = shares[i][0] 
			if i != j: prod *= Decimal(Decimal(xi)/(xi-xj)) 
				
		prod *= yj 
		sums += Decimal(prod) 
		
	return int(round(Decimal(sums),0)) 

def polynom(x,coeff): 
	
	# Evaluates a polynomial in x 
	# with coeff being the coefficient 
	# list 
	return sum([x**(len(coeff)-i-1) * coeff[i] for i in range(len(coeff))]) 

def coeff(t,secret): 
	
	# Randomly generate a coefficient 
	# array for a polynomial with 
	# degree t-1 whose constant = secret''' 
	coeff = [random.randrange(0, field_size) for _ in range(t-1)] 
	coeff.append(secret) 
	
	return coeff 

def generateShares(n,m,secret): 
	
	# Split secret using SSS into 
	# n shares with threshold m 
	cfs = coeff(m,secret) 
	shares = [] 
	
	for i in range(1,n+1): 
		r = random.randrange(1, field_size) 
		shares.append([r, polynom(r,cfs)]) 
	
	return shares 

def start():
    secret = int(secretEntry.get())
    n = int(shareNumberEntry.get())
    t = int(combineShareEntry.get())
    shares = generateShares(n, t, secret)
    print("shares",shares)
    for i in range(n):
        label = tk.Label(text=i)
        label.pack()
        entry = tk.Text(width=50,height=1)
        entry.insert(INSERT, str(shares[i]))
        entry.insert(END, " ")
        entry.pack()


def crack():
    pool1 =[]
    pool2 = []
    final = []

    numberOfSharesRow = int(numberOfShares.get())
    #print(numberOfSharesRow)
    for entry in entries:
        pool = []
        print(entry.get())
        entry = entry.get()
        x = entry.split(",")
        print(x)
        pool.append(int(x[0]))
        pool.append(int(x[1]))        
        print(entry)
        final.append(pool)

    print("Final",final)
    answer = reconstructSecret(final)
    answer = tk.Label(text="Secret = "+ str(answer))
    answer.pack()

def generateRows():
    numberOfSharesRow = int(numberOfShares.get())
    for i in range(numberOfSharesRow):
        en = Entry(root)
        en.grid(row=i+1, column=0)
        entries.append(en)
# Driver code 
if __name__ == '__main__': 
    # (3,5) sharing scheme t=number of combined shares , n=number of shares
    t,n = 3, 3
    secret = 1234
    print('Original Secret:', secret) 

    # Phase I: Generation of shares 
    shares = generateShares(n, t, secret) 
    print('\nShares:', *shares) 

    # Phase II: Secret Reconstruction 
    # Picking t shares randomly for 
    # reconstruction 
    pool = random.sample(shares, t) 
    print('\nCombining shares:', pool) 
    print("Reconstructed secret:", reconstructSecret(pool))

    combineNumber = tk.Label(text="Number of Combined Shares")
    combineNumber.pack() 
    combineShareEntry = tk.Entry(width=20)
    combineShareEntry.pack()


    shareNumber = tk.Label(text="Number of Shares")
    shareNumber.pack()
    shareNumberEntry = tk.Entry(width=20)
    shareNumberEntry.pack() 
    
   
    secretLabel = tk.Label(text="Secret")
    secretLabel.pack()
    secretEntry = tk.Entry(width=20)
    secretEntry.pack()
    

    generateButton = tk.Button(command=start,text="Generate Shares")
    generateButton.pack()


    numberOfShares = tk.Label(text="Input Number of shares")
    numberOfShares.pack() 
    numberOfShares = tk.Entry(width=20)
    numberOfShares.pack()
    

    rowButton = tk.Button(command=generateRows,text="Generate Rows")
    rowButton.pack()
    


    crackButton = tk.Button(command=crack,text="Crack Code")
    crackButton.pack()

    window.mainloop()
