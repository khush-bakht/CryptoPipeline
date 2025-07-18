class DataSaver:
    @staticmethod
    def save_to_csv(df, output_path):
        df.to_csv(output_path, index=False)