# SI 201 HW4 (Library Checkout System)
# Your name:
# Your student id:
# Your email:
# Who or what you worked with on this homework (including generative AI like ChatGPT):
# If you worked with generative AI also add a statement for how you used it.
# e.g.:
# Asked ChatGPT for hints on debugging and for suggestions on overall code structure
#
# Did your use of GenAI on this assignment align with your goals and guidelines in your Gen AI contract? If not, why?
#
# --- ARGUMENTS & EXPECTED RETURN VALUES PROVIDED --- #
# --- SEE INSTRUCTIONS FOR FULL DETAILS ON METHOD IMPLEMENTATION --- #

from bs4 import BeautifulSoup
import re
import os
import csv
import unittest
import requests  # kept for extra credit parity


# IMPORTANT NOTE:
"""
If you are getting "encoding errors" while trying to open, read, or write from a file, add the following argument to any of your open() functions:
    encoding="utf-8-sig"
"""


def load_listing_results(html_path) -> list[tuple]:
    """
    Load file data from html_path and parse through it to find listing titles and listing ids.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples containing (listing_title, listing_id)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE

    with open(html_path, 'r', encoding='utf-8-sig') as f:
        html = f.read()

        soup = BeautifulSoup(html, 'html.parser')


        results = []

        title_divs = soup.find_all('div', attrs={'data-testid': 'listing-card-title'})

        for div in title_divs:
            title = div.get_text(strip=True)

            div_id = div.get('id', '')  # e.g. "title_1944564"
            listing_id = div_id.split('_')[-1]  # e.g. "1944564"

            if title and listing_id:
                results.append((title, listing_id))

        return results



    # ==============================
    pass
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def get_listing_details(listing_id) -> dict:
    """
    Parse through listing_<id>.html to extract listing details.

    Args:
        listing_id (str): The listing id of the Airbnb listing

    Returns:
        dict: Nested dictionary in the format:
        {
            "<listing_id>": {
                "policy_number": str,
                "host_type": str,
                "host_name": str,
                "room_type": str,
                "location_rating": float
            }
        }
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    base_dir = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(base_dir, "html_files", f"listing_{listing_id}.html")

    with open(file_path, "r", encoding="utf-8-sig") as f:
        html = f.read()

        soup = BeautifulSoup(html, "html.parser")

    # Find to policy number

    policy_number = "Exempt"

    policy_div = soup.find("div", class_="_1k8vduze")
    if policy_div:
        lines = policy_div.get_text("\n", strip=True).split("\n")  # split into lines

        for line in lines:
            line = line.strip()
            # Check for STR or digits
            if re.match(r"(STR|[0-9]{4}).*", line):
                policy_number = line
                break
            elif "pending" in line.lower():
                policy_number = "Pending"
                break
        

    # Find host type

    text = soup.get_text()
    if "superhost" in text.lower():
        host_type = "Superhost"
    else:
        host_type = "regular"

    # Find host name

    host_name = "" 
    
    host_text = soup.find(string=re.compile("Hosted by"))
    if host_text:
        host_name = host_text.replace("Hosted by", "").strip()

    # Find room type 

    room_type = "Entire Room"

    subtitle = soup.find("h2")
    if subtitle:
        text = subtitle.get_text().lower()
        if "private" in text:
            room_type = "Private Room"
        elif "shared" in text:
            room_type = "Shared Room"

    # Find location

    location_rating = 0.0

    rating_tag = soup.find("span", class_="_17p6nbba")  
    if rating_tag:
        rating_str = rating_tag.get_text(strip=True)  
        rating_str = rating_str.replace("·", "")      
        location_rating = float(rating_str)

    return {
        listing_id: {
           "policy_number": policy_number,
           "host_type": host_type, 
           "host_name": host_name, 
           "room_type": room_type, 
           "location_rating": location_rating 
    }
        }


    # ==============================
    pass
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def create_listing_database(html_path) -> list[tuple]:
    """
    Use prior functions to gather all necessary information and create a database of listings.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples. Each tuple contains:
        (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE


    # ==============================
    pass
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def output_csv(data, filename) -> None:
    """
    Write data to a CSV file with the provided filename.

    Sort by Location Rating (descending).

    Args:
        data (list[tuple]): A list of tuples containing listing information
        filename (str): The name of the CSV file to be created and saved to

    Returns:
        None
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    outFile = open(filename, 'w')
    csv_writer = csv.writer(outFile)

    # write header row
    csv_writer.writerow(["Listing Title", "Listing ID", "Policy Number", "Host Type", "Host Name", "Room Type", "Location Rating"])

    # sort data (by location rating)
    sorted_data = sorted(data, key = lambda t:t[6], reverse = True)

    # loops through tuple list
    for entry in sorted_data:
        csv_writer.writerow([entry[0], entry[1], entry[2], entry[3], entry[4], entry[5], entry[6]])

    outFile.close()
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def avg_location_rating_by_room_type(data) -> dict:
    """
    Calculate the average location_rating for each room_type.

    Excludes rows where location_rating == 0.0 (meaning the rating
    could not be found in the HTML).

    Args:
        data (list[tuple]): The list returned by create_listing_database()

    Returns:
        dict: {room_type: average_location_rating}
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    
    d = {}
    counts = {}

    for entry in data:

        # gets room_type and location_rating from entry
        room_type = entry[5]
        location_rating = entry[6]

        # prevents location ratings of 0.0 from being included
        if location_rating == 0.0:
            continue

        if room_type not in d:
            d[room_type] = location_rating
            counts[room_type] = 1
        else:
            d[room_type] = d[room_type] + location_rating
            counts[room_type] += 1
    
    # comverts values in d from totals to averages
    for room_type in d:
        d[room_type] = d[room_type] / counts[room_type]

    return d


    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def validate_policy_numbers(data) -> list[str]:
    """
    Validate policy_number format for each listing in data.
    Ignore "Pending" and "Exempt" listings.

    Args:
        data (list[tuple]): A list of tuples returned by create_listing_database()

    Returns:
        list[str]: A list of listing_id values whose policy numbers do NOT match the valid format
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    pass
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


# EXTRA CREDIT
def google_scholar_searcher(query):
    """
    EXTRA CREDIT

    Args:
        query (str): The search query to be used on Google Scholar
    Returns:
        List of titles on the first page (list)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    pass
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


class TestCases(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.abspath(os.path.dirname(__file__))
        self.search_results_path = os.path.join(self.base_dir, "html_files", "search_results.html")

        self.listings = load_listing_results(self.search_results_path)
        self.detailed_data = create_listing_database(self.search_results_path)

    def test_load_listing_results(self):
        # TODO: Check that the number of listings extracted is 18.
        self.assertEqual(len(self.listings), 18)

        # TODO: Check that the FIRST (title, id) tuple is  ("Loft in Mission District", "1944564").
        self.assertEqual(self.listings[0],("Loft in Mission District", "1944564"))
        pass

    def test_get_listing_details(self):
        html_list = ["467507", "1550913", "1944564", "4614763", "6092596"]

        # TODO: Call get_listing_details() on each listing id above and save results in a list.

        test_list = [get_listing_details("467507"),get_listing_details("1550913"),get_listing_details("1944564"),get_listing_details("4614763"),get_listing_details("6092596")]

        # TODO: Spot-check a few known values by opening the corresponding listing_<id>.html files.
        # 1) Check that listing 467507 has the correct policy number "STR-0005349".
        self.assertEqual(test_list[0]["467507"]["policy_number"],"STR-0005349")
        # 2) Check that listing 1944564 has the correct host type "Superhost" and room type "Entire Room".
        self.assertEqual(test_list[2]["1944564"]["host_type"],"Superhost")
        self.assertEqual(test_list[2]["1944564"]["room_type"],"Entire Room")
        # 3) Check that listing 1944564 has the correct location rating 4.9.
        self.assertAlmostEqual(test_list[2]["1944564"]["location_rating"],4.9)

        pass

    def test_create_listing_database(self):
        # TODO: Check that each tuple in detailed_data has exactly 7 elements:
        # (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)

        # TODO: Spot-check the LAST tuple is ("Guest suite in Mission District", "467507", "STR-0005349", "Superhost", "Jennifer", "Entire Room", 4.8).
        pass

    def test_output_csv(self):
        out_path = os.path.join(self.base_dir, "test.csv")

        # TODO: Call output_csv() to write the detailed_data to a CSV file.
        output_csv(create_listing_database(), "test.csv")

        # TODO: Read the CSV back in and store rows in a list.
        listings = load_listing_results("test.csv")

        # TODO: Check that the first data row matches ["Guesthouse in San Francisco", "49591060", "STR-0000253", "Superhost", "Ingrid", "Entire Room", "5.0"].
        self.assertEqual(self.listings[1],("Guesthouse in San Francisco", "49591060", "STR-0000253", "Superhost", "Ingrid", "Entire Room", "5.0"))

        os.remove(out_path)

    def test_avg_location_rating_by_room_type(self):
        # TODO: Call avg_location_rating_by_room_type() and save the output.
        output = avg_location_rating_by_room_type(get_listing_details())
        # TODO: Check that the average for "Private Room" is 4.9.
        self.assertEqual(output["Private Room"], 4.9)

    def test_validate_policy_numbers(self):
        # TODO: Call validate_policy_numbers() on detailed_data and save the result into a variable invalid_listings.
        # TODO: Check that the list contains exactly "16204265" for this dataset.
        pass


def main():
    detailed_data = create_listing_database(os.path.join("html_files", "search_results.html"))
    output_csv(detailed_data, "airbnb_dataset.csv")
    print(get_listing_details(31057117))


if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)