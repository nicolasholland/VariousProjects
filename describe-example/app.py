import pandas as pd

def main():
    df = pd.read_json('input/input.json')
    processed = df.describe()
    processed.to_json('output/processed.json')

if __name__ == '__main__':
    main()
