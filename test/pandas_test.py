import pandas as pd

def test_pd():
    results = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]

    df = pd.DataFrame(results, columns=["x", "y", "z"])

    print(df)

    df.to_csv('test/test.csv', index=False)

    pass

if __name__ == '__main__':
    test_pd()