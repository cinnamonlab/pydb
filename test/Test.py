
values = ["a", "b", "c"]
t = ["%s"] * len(values)
print(t)


print (', '.join(map(str, values)))
print(["'{}'".format(x) for x in values])