sizes = ["Large", "Large", "Small"]


large = 0
medium = 0
small = 0
for data in sizes:
    if data == "Large":
        large += 1
    if data == "Medium":
        medium += 1
    if data == "Small":
        small += 1

print("Large: ", large)
print("Medium: ", medium)
print("Small: ", small)
    