columns={'check_constraints': {'role': ['staff', 'admin']}, 'columns': ['staff_name', 'email', 'phone_number', 'address', 'role', 'join_date', 'password']}
columns1={'check_constraints': {'condition': ['New', 'Old'], 'status': ['Available', 'pending', 'issued']}, 'columns': ['book_id', 'condition', 'status']}
constraints=columns1.get('check_constraints',[])
print(f"the constrainst are {constraints} and it's length is {len(constraints)}")
total_constraints=[]
for key in constraints:
    print(key)
    