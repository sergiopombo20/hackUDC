import magic
import csv

def csv_is_valid(file_path):
    def is_csv_magic(file_path):
        """
        Use libmagic to check the file's MIME type.
        """
        try:
            mime_type = magic.from_file(str(file_path), mime=True)
            # Allow text types, but you can tighten the check as needed.
            return mime_type == "text/csv" or mime_type.startswith("text/")
        except Exception as e:
            print(f"Magic check failed: {e}")
            return False

    def is_csv_content(file_path):
        pass
        ### TODO: Implement this function
            # """
            # Try parsing the file with the csv module.
            # If it parses a few rows without error, assume it's a CSV.
            # """
            # try:
            #     with open(file_path, 'r', encoding='utf-8') as f:
            #         reader = csv.reader(f)
            #         # Attempt to read a few rows
            #         for _ in range(3):
            #             next(reader)
            #     return True
            # except Exception as e:
            #     print(f"CSV parsing error: {e}")
            #     return False

    return file_path.name.lower().endswith('.csv') and is_csv_magic(file_path) #and is_csv_content(file_path)