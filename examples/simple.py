from qumcat import Qumcat

if __name__ == "__main__":
    q = Qumcat.generate_mct_cases(3, 1)
    print(len(q.circuits))
