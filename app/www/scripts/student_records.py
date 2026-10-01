#---------------------
#python essentials 8.7
#---------------------

#These are tuples the information cannot be changed

student_1 = ("Alice Johnson", 20, "A")
student_2 = ("Ben Carter", 22, "B")
student_3 = ("Chloe Davis", 21, "A")
student_4 = ("Daniel Evans", 23, "C")
student_5 = ("Alice Johnson", 20, "A")  # duplicate record, used below

# A collection of existing tuples
students = (student_1, student_2, student_3, student_4, student_5)

print("All student records:")
for name, age, grade in students:
    print(f"  {name}, age {age}, grade {grade}")



# count() and index()
occurrences = students.count(student_5)
print(f"\n'{student_5[0]} appears {occurrences} times in the records")


position = students.index(student_3)
print(f"'{student_3[0]}' is record number {position} (0-indexed)")

#-----
#Sets
#-----
# A set automatically drops duplicates and has no guaranteed order


student_ids = {101, 102, 103, 101, 104}  # 101 typed twice
print(f"\nUnique student IDs: {student_ids}")
# Even though 101 appears twice in the literal, the set keeps only one copy.

alice_courses = {"Maths", "Physics", "Computer Science"}
ben_courses = {"Physics", "Chemistry", "Computer Science", "Biology"}

print(f"Alice's courses: {alice_courses}")
print(f"Ben's courses:   {ben_courses}")


# ---------------------------------------------------------------------------
# 4. SET OPERATIONS — union, intersection, difference
# ---------------------------------------------------------------------------
all_courses = alice_courses | ben_courses      # union: everything in either set
shared_courses = alice_courses & ben_courses    # intersection: only in both
only_alice = alice_courses - ben_courses        # difference: in Alice's, not Ben's
only_ben = ben_courses - alice_courses          # difference the other way round

print(f"\nAll courses between them (union):      {all_courses}")
print(f"Courses they share (intersection):     {shared_courses}")
print(f"Courses only Alice takes (difference): {only_alice}")
print(f"Courses only Ben takes (difference):   {only_ben}")

#add() and remove() - note add() goes in different order each time
alice_courses.add("English")
print(f"Alice's new courses: {alice_courses}")

alice_courses.remove("English")
print(f"Alice's original courses: {alice_courses}")


# ----------------------------------
#Frozen Sets — immutable sets of data
# ------------------------------------
# A frozenset behaves exactly like a set, except it's immutable — no add(),
# remove(), or any operation that changes it in place. Useful for something
# that must never be edited after creation, like a fixed list of core
# subjects every student is required to take.

core_subjects = frozenset({"Maths", "English", "Science"})
print(f"\nCore subjects (frozen): {core_subjects}")

try:
    core_subjects.add("Art")   # this will fail — frozensets have no add()
except AttributeError as e:
    print(f"Can't modify a frozenset: {e}")

# Frozensets still support the read-only set operations (union, intersection,
# etc.) — they just return a brand new frozenset rather than changing anything
# in place.
alice_frozen = frozenset(alice_courses)
extended = alice_frozen | frozenset({"Art"})
print(f"Original frozenset unchanged: {alice_frozen}")
print(f"New frozenset from the union: {extended}")

# One practical reason to reach for a frozenset: because it's immutable, it's
# HASHABLE — which means, unlike a normal set, it can be used as a dictionary
# key or stored inside another set. A plain (mutable) set can't do this.
schedules = {
    frozenset({"Maths", "Physics"}): "Group A",
    frozenset({"Chemistry", "Biology"}): "Group B",
}
print(f"\nSchedule lookup: {schedules[frozenset({'Maths', 'Physics'})]}")