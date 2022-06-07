a = "a"
b = "b"
up_s = ((5, "a"), (13, "a"), (20, "a"), (21, "a"), (29, "a"), (33, "a"), (42, "a"), (46, "a"))
uh_s = ((2, "b"), (10, "b"), (14, "b"), (15, "b"), (24, "a"), (26, "b"), (38, "b"), (40, "b"))
gp_s = ((8, "a"), (16, "a"), (17, "a"), (18, "a"), (22, "a"), (32, "b"), (44, "a"), (48, "a"))
gh_s = ((6, "b"), (7, "b"), (28, "b"), (31, "b"), (34, "b"), (35, "b"), (37, "b"), (43, "b"))
pp_s = ((3, "a"), (9, "a"), (19, "a"), (25, "a"), (30, "a"), (39, "a"), (41, "a"), (47, "a"))
ph_s = ((1, "a"), (4, "b"), (11, "b"), (12, "b"), (23, "b"), (27, "b"), (36, "b"), (45, "b"))
# answers = tuple()
# for n in range(48):
#     user_input = ""
#     while (user_input != "a") and (user_input != "b"):
#         user_input = input(f"Вопрос № {n + 1} ").lower()
#     answers = answers + tuple(user_input)

# Jolanta
answers = (a, b, a, a, a, b, b, b, b, b, b, b, b, b, b, b, a,
           a, a, a, b, b, b, a, a, a, b, b, a, b, b, a, a, b,
           a, a, a, b, b, b, a, a, b, a, b, a, b, a)

# Ilya
# answers = (b, b, a, a, a, a, a, a, b, a, a, b, a, b, b, b, a, a,
#            a, b, a, b, b, a, b, a, b, a, b, b, a, a, b, a, b, a, a,
#            b, b, a, a, a, a, a, a, b, b, b)

def count_points(samples, user_answers):
    points = 0
    for item in samples:
        if user_answers[item[0]-1] == item[1]:
            points += 1
    return points


up = count_points(up_s, answers)
uh = count_points(uh_s, answers)
gp = count_points(gp_s, answers)
gh = count_points(gh_s, answers)
pp = count_points(pp_s, answers)
ph = count_points(ph_s, answers)
kn = gp + up
h = uh + gh + ph
p = up + gp + pp
summary = h - p

print(f"УП = {up}")
print(f"УХ = {uh}")
print(f"ГП = {gp}")
print(f"ГХ = {gh}")
print(f"ПП = {pp}")
print(f"ПХ = {ph}")
print(f"КН = {kn}")
print(f"П = {p}")
print(f"Х = {h}")
print(f"ИТОГ = {summary}")
