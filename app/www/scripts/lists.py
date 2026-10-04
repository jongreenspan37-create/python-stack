# Practice: Python lists (append, nesting, indexing). Run directly; not an API endpoint.
mylist =[1,2,3]
print(mylist)
mylist.append(4)
print(mylist)
mylist.append('hello')
print(mylist)
print(mylist[4])

mynewlist=[1,['one','two','three'],3]
print(mynewlist)
print(mynewlist[1][2])

mylist.pop(3)
print(mylist)

dict={'one':1,'two':2,'three':3}
print(dict.keys())
print(list(dict.values()))
print(dict['one'])

complexdict={1:[1,2,3],2:[4,5,6],3:[7,8,9],4:[10,11,12]}
print(complexdict[2][1])

listdict=[{'one':1,'two':2,'three':3},{'four':4,'five':5,'six':6}]
print(listdict[1]['five'])


dataexample= [
    {'table':'users','columns':['id','LastName','FirstName','email','role_id']},
    {'table':'roles','columns':['id','name']} 
     ]

for t in dataexample:
    print(t['table'])
    for c in t['columns']:
        print(c)

schema = {
    'users' :{
        'columns': ['id','LastName','FirstName','email','role_id'],
        'foreign_keys': {'role_id':'roles.id'}
    },   

    'roles' :{
        'columns': ['id','name'],
        'foreign_keys': {},
    },
}