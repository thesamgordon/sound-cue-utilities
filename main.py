from file_handler import read_excel_data
from snippet_generator import generate_snippets
from qlab_network_generator import generate_network_cues
import os
from dotenv import load_dotenv
load_dotenv()

def main():
    xlsx_file = os.getenv("FILE_NAME")

    skip_rows = int(os.getenv("ROW_START", "0")) - 1
    if skip_rows < 0:
        skip_rows = 0

    identifying_character = os.getenv("IDENTIFYING_CHARACTER", "X")

    print(f"Choose cue generation method:")
    print("1. Generate X32 Snippets")
    print("2. Generate QLab Cues")
    method = os.getenv("METHOD", "SNIPPET")

    use_dca = os.getenv("USE_DCA", "false").lower() in ["true", "1", "yes"]
    dca_identifier = os.getenv("DCA_IDENTIFIER", "/") if use_dca else None

    show_file_name = xlsx_file.replace(".xlsx", "")
    data_frame = read_excel_data(xlsx_file, skip_rows)
        
    if method == "SNIPPET":
        generate_snippets(data_frame, show_file_name, "output", identifying_character, use_dca, dca_identifier)
    elif method == "NETWORK":
        generate_network_cues(data_frame, identifying_character, dca_identifier, "1")
    else:
        print("Invalid method specified in .env file. Please choose either 'SNIPPET' or 'NETWORK'.")

if __name__ == "__main__":
    main()

