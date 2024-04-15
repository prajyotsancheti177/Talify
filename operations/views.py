from django.shortcuts import render
import pandas as pd
import requests
from datetime import datetime

def create_ledger(name):
    # XML payload for ledger creation
    xml_data = f"""
            <ENVELOPE>
                <HEADER>
                    <TALLYREQUEST>Import Data</TALLYREQUEST>
                </HEADER>
                <BODY>
                    <IMPORTDATA>
                        <REQUESTDESC>
                            <REPORTNAME>All Masters</REPORTNAME>
                        </REQUESTDESC>
                        <REQUESTDATA>
                            <TALLYMESSAGE xmlns:UDF="TallyUDF">
                                <LEDGER NAME="Customer ABC">
                                    <NAME>{name}</NAME>
                                    <PARENT>Investments</PARENT>
                                </LEDGER>
                            </TALLYMESSAGE>
                        </REQUESTDATA>
                    </IMPORTDATA>
                </BODY>
            </ENVELOPE>
    """
    
    # Tally Prime API endpoint
    api_endpoint = 'http://localhost:9000/api/data'

    # Send POST request to Tally Prime API
    response = requests.post(api_endpoint, data=xml_data)
    
    # Print response content
    print(response.text)

def create_voucher(date,dr_amount,cr_amount,dr,cr):
    xml_data = f"""
                <ENVELOPE>
                    <HEADER>
                        <VERSION>1</VERSION>
                        <TALLYREQUEST>Import</TALLYREQUEST>
                        <TYPE>Data</TYPE>
                        <ID>Vouchers</ID>
                    </HEADER>
                    <BODY>
                        <DESC></DESC>
                        <DATA>
                            <TALLYMESSAGE>
                                <VOUCHER>
                                    <DATE>{date}</DATE>
                                    <VOUCHERTYPENAME>Journal</VOUCHERTYPENAME>
                                    <VOUCHERNUMBER>1</VOUCHERNUMBER>
                                    <PERSISTEDVIEW>Accounting Voucher View</PERSISTEDVIEW>
                                    <ISINVOICE>No</ISINVOICE>
                                    <LEDGERENTRIES.LIST>
                                        <LEDGERNAME>{dr}</LEDGERNAME>
                                        <ISDEEMEDPOSITIVE>Yes</ISDEEMEDPOSITIVE>
                                        <ISPARTYLEDGER>Yes</ISPARTYLEDGER>
                                        <ISLASTDEEMEDPOSITIVE>Yes</ISLASTDEEMEDPOSITIVE>
                                        <AMOUNT>{dr_amount}</AMOUNT>  <!-- Change to positive -->
                                    </LEDGERENTRIES.LIST>
                                    <LEDGERENTRIES.LIST>
                                        <LEDGERNAME>{cr}</LEDGERNAME>
                                        <ISDEEMEDPOSITIVE>No</ISDEEMEDPOSITIVE>
                                        <AMOUNT>{cr_amount}</AMOUNT>  <!-- Adjusted to match debit -->
                                    </LEDGERENTRIES.LIST>
                                </VOUCHER>
                            </TALLYMESSAGE>
                        </DATA>
                    </BODY>
                </ENVELOPE>
    """
    
    print(xml_data)
        
    # Tally Prime API endpoint
    api_endpoint = 'http://localhost:9000/api/data'

    # Send POST request to Tally Prime API
    response = requests.post(api_endpoint, data=xml_data)
    
    # Print response content
    print(response.text)    


def home(request):

    if request.method == 'POST':
        print(request.POST)
        excel_file = request.FILES['excel_file']
        df = pd.read_excel(excel_file)
        print(df)

        for index, row in df.iterrows():
            name = row['Symbol']
            name = "Share - "+name
            create_ledger(name)

        for index, row in df.iterrows():
            name = row['Symbol']
            date = row['Trade Date']
            amount = row['Quantity'] * row['Price']
            if row['Trade Type'] == 'buy':
                dr = 'Share - '+name
                cr = 'Zerodha A/c'
                dr_amount = -1 * amount
                cr_amount = amount
            elif row['Trade Type'] == 'sell':
                dr = 'Zerodha A/c'
                cr = 'Share - '+name
                dr_amount = -1 * amount
                cr_amount = amount        
            formatted_date = date.strftime('%Y%m%d')
            create_voucher(formatted_date,dr_amount,cr_amount,dr,cr)

    return render(request, 'home.html')
