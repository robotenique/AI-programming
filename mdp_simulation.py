# Define the policy here
TRANSITION = {"1": [0.2, 0.8] , "2": [0.2, 0.8], "3": [0.0]}
REWARD = {"1|0.2": -1, "1|0.8": -2, "2|0.2": -2, "2|0.8": -1}
MAPPER = {"1|0.2": 0, "1|0.8": 1, "2|0.2": 1, "2|0.8": 0}

def main():
    values = [[0, 0, 0]]
    k = 1
    final_k = 100
    epsilon = 1e-3
    desc = 0.5
    while True:
        temp_val = [0]*3
        for s in range(len(values[0])):
            temp_val[s] = sum(t*(REWARD.get(str(s+1)+"|"+str(t), 0.0) + desc*values[k-1][MAPPER.get(str(s+1)+"|"+str(t), 2)]) for t in TRANSITION[str(s+1)])
        print(f"Val {k} = {temp_val}")
        values.append(temp_val)
        if all(abs(values[k][i] - values[k-1][i]) <= epsilon  for i in range(0, 3)):
            break
        k += 1


    contA_1 = 0.8*(-2 + values[k][1]) + 0.2*(-1 + values[k][0])
    contB_1 = 0.1*(0 + values[k][2]) + 0.9*(-1 + values[k][0])
    contA_2 = 0.8*(-1 + values[k][0]) + 0.2*(-2 + values[k][1])
    contB_2 = 0.1*(0 + values[k][2]) + 0.9*(-2 + values[k][1])
    pol_1 = "A" if contA_1 > contB_1 else "B"
    pol_2 = "A" if contA_2 > contB_2 else "B"
    print(f"max({contA_1, contB_1})")
    print(f"max({contA_2, contB_2})")
    print(f"Nova política: [{pol_1}, {pol_2}, T]")




if __name__ == '__main__':
    main()
