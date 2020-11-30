import sys

def check_sheet_id(link):
    # Read the Spreadsheet ID from the config file
    # TODO: Ensure this is a valid spreadsheet link, not just empty
    try:  # Check that the link to the spreadsheet is not empty
        assert link != ""
        bench_spreadsheet_id = link[link.find("/d/") + 3:link.find("/edit")]  # Extract the id from the
        return bench_spreadsheet_id  # full link
    except AssertionError:
        f = open("error.txt", "w")
        f.write(
            "You did not input a 'link_to_sheet' in your config file, make sure to input your values into the "
            "config.json.")
        f.close()
        print("You did not input a 'link_to_sheet' in your config file, make sure to input your values into the "
                "config.json.")
        input("Press 'Enter' to exit")
        sys.exit()

def handle_error(error_type, error=None, r=" "):
    if error:
        message = "Sheets API: " + error._get_reason()
    else:
        if error_type == "path":
            message = "Could not find the path you specified, make sure you input the correct one"
        elif error_type == "range":
            message = "Invalid sheet range: " + r
        elif error_type == "range_too_small":
            message = "Range size mismatched, check that each list of ranges has the same number of cells referenced."
    f = open("error.txt", "w")
    f.write(message + "\nIf you are not sure what this means, try looking into the readme.")
    f.close()
    print(message)
    input("Press 'Enter' to exit")
    sys.exit()


def avg(scores):
    if len(scores) == 0:
        return 0
    return round(sum(scores) / len(scores), 1)