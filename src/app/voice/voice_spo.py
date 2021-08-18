from app.spo.SPODetector import get_oie_triplets, get_svo_from_triplet

text = "She returned the computer after noticing the damage."
triplets = get_oie_triplets(text)
for triplet in triplets:
   svo = get_svo_from_triplet(triplet)
print(svo)

subject = svo['Subject']
print('subject index: ')
sub_index = text.index(subject)
print(sub_index)

objectClause = svo['Object Clauses']
obj = ''
for i in objectClause:
    obj = obj + i
print('object index: ')
obj_index = text.index(obj)
print(obj_index)

if sub_index < obj_index:
    print("Active")
if obj_index < sub_index:
    print("Passive")