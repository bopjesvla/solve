x = np.array(list(range(7)))

changes = [([], []), ([], []), ([2, 6], [6, 2]), ([0, 1], [1,0]), ([1, 2, 3], [2, 3, 1]), ([], []), ([4, 5, 6], [5, 6, 4])]

x = np.array([[2.0,2.3333333,2.3333333,2.3333333,2.3333333,2.3333333,2.3333333],[2.3333333,2.8150132,2.3333333,2.497264,2.8150132,2.3333333,0.87271],[2.8748512,0.8150131,0.87271,2.8748512,2.8748512,2.8128717,2.8748512],[0.87056863,0.8748513,0.87271,3.3454676,3.3454676,3.3454676,3.3454676],[0.8748513,1.3454676,0.8748513,0.87271,4.0107064,4.0107064,4.0107064],[0.8748513,1.3454676,0.87699264,0.8748513,2.0107067,4.0107064,6.006424],[0.8748513,1.3454676,0.87913394,0.87699264,7.0021415,2.0107067,3.0107067],[0.8748513,1.3454676,0.87699264,0.87913394,8.002141,2.0107067,2.0107067]])

y = np.array([[2.0,2.3333333,2.3333333,2.3333333,2.3333333,2.3333333,2.3333333],[2.3333333,2.8150132,2.3333333,2.497264,2.8150132,2.3333333,0.87271],[2.8748512,0.8150131,0.87271,2.8748512,2.8748512,2.8128717,2.8748512],[0.87056863,0.8748513,0.87271,3.3454676,3.3454676,3.3454676,3.3454676],[0.8748513,1.3454676,0.8748513,0.87271,4.0107064,4.0107064,4.0107064],[0.8748513,1.3454676,0.87699264,0.8748513,2.0107067,4.0107064,6.006424],[0.8748513,1.3454676,0.87913394,0.87699264,7.0021415,2.0107067,3.0107067],[0.8748513,1.3454676,0.87699264,0.87913394,8.002141,2.0107067,2.0107067]])

for i, (frm, to) in enumerate(changes):
    x[i:,frm] = x[i:, to]
