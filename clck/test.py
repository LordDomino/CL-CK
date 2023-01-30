from emics import Pattern

pattern = Pattern("h", "[h]j|h.j|h[j]")

print(pattern.execute())