# status-invest-scraping :hourglass_flowing_sand:
This is a Python script that scrapes information about Stocks or REITs from the statusinvest.com.br website. It retrieves data such as stock price, P/VP (Price-to-Net Asset Value Ratio), P/L (Price-to-Earnings Ratio), DY (Dividend Yield) for a list of specified codes

## Requirements
The script requires the following Python packages to be installed:

- Requests
- BeautifulSoup
- Pandas
- PyQt5
- Openpyxl

You can install these dependencies using the following command:
```
pip install -r requirements.txt
```

## Usage

1. Launch the FII Info App by running the `app.py` script.
2. Enter the FII codes in the provided text box and click enter after each FII code to add them.
3. Press the "Get Information" button to retrieve the information for the entered codes.
4. The progress bar will indicate the progress of the retrieval process.
5. Once the retrieval process is complete, a save dialog will appear.
6. Choose a location and provide a filename to save the retrieved information as an Excel file.
7. If there were any errors or missing data during the retrieval process, warning messages will be displayed.
8. Click "OK" to dismiss the warning messages.
9. The application can be closed by clicking the close button or pressing the "Esc" key.

## Notes :warning:

- The script assumes the website structure remains the same. If there are any changes to the website's HTML structure or class names, the script may need to be updated accordingly.
- The script only uses public information
- It's important to respect website scraping policies and avoid overloading the website with frequent requests. Consider adding delays between requests if scraping a large number of Stocks/REITs.

## Contributing
Contributions to the FII Info App are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.