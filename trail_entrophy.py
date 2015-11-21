import math

values = [32,48,48,50,50,52,48,50,22]
# values = [100,1000,10000,10,10,10]
# entropy = 0.000
# for i in values:
#     p = float(i) / len(values)
#     if p > 0:
#         entropy += - p*math.log(p)
#
# print(entropy)
sum = 0
for i in values:
    sum += i

mean = sum/len(values)
print("mean " + str(mean))
sum_of_diff = 0
for i in values:
    sum_of_diff += (i - mean)*(i - mean)

print(math.sqrt(sum_of_diff/(len(values)-1)))