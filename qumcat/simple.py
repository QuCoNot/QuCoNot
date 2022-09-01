from qumcat import Qumcat

if __name__ == "__main__":
    print("controls_no : ", 5, ", max_ancillas : ", 3)

    mct = Qumcat.generate_mct_cases(5, 3)
    print("generated cases :", len(mct.circuits))

    for idx, qc in enumerate(mct.circuits):

        print("Circuit-", idx)
        print("depth: ", qc.depth())
        print(dict(qc.count_ops()))
        print(" ")
