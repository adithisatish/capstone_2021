import csv

file = open("sample.txt","r")
text = file.read().split(".")[:-1]
file.close()
k=0
processed = []
for i in range(len(text)):
    words = text[i].strip().split()
    if len(words) <= 4:
        continue
    processed.append(text[i].strip())

# print(processed)

with open("similes.csv","a+", newline='') as similes:
    writer = csv.writer(similes)
    for i in processed:
        writer.writerow([i,"N"])
