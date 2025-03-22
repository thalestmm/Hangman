import pandas as pd

# Pre-process a base .txt file containing all words
# TODO: Change the output file to a sqlite DB
# TODO: Add cmdline args

def main():
    we = WordsEditor("words.txt")
    we.execute()


class WordsEditor:
    def __init__(self, target_file: str) -> None:
        self.filepath = target_file
        self.df = pd.read_table(self.filepath)

    def letter_counter(self):
        self.df["letters"] = self.df["word"].str.len()

    def identify_symbols(self):
        symbols = "Á|Â|Ã|À|É|Ê|Í|Ó|Õ|Ô|Ç"
        self.df["has_symbol"] = (self.df["word"].str.contains(symbols))
        pass

    def upper_everything(self):
        self.df["word"] = self.df["word"].str.upper()
        pass

    def export(self):
        self.df.to_csv("game_ready.csv", index=False)

    def execute(self):
        self.letter_counter()
        self.upper_everything()
        self.identify_symbols()
        self.export()


if __name__ == "__main__":
    main()