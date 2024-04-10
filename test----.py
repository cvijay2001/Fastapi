import requests
import json

url_1 = "http://192.168.0.100:8080"
url_2 = "http://192.168.6.105:5000"

class TestRequest():
    def test_add_cost(self):
        url = url_2+'/add-cost'
        print(url)
        headers = {
        'content-type': "application/form-data",
        'cache-control': "no-cache",
        }   
        # data = {'selectedOfftaker':161,'selectedBorrower':52,'selectedCollateral':1,'contractNumber':'P1233adv45r','contractDate':'2021-08-01','totalQuantity':100,'selectedUnit':1,'deliveryMonth':'null','selectedPriceType':'null','price':'null','conversionRate':'null','finalPrice':'null','contractValue':'null','paymentTerms':'null','agent':'null','quality':'null','terms':'null','arbitration':'null','comments':'null','status':'null','selectedDetails':'offtaker contract','OfftakerContractDocuments':'null','clientId':1,'userId':1,'moduleId':12,'tabId':30,}
        data = {'selectedBorrower': '52', 'selectedFacility': '40', 'selectedCost': '1', 'amount': '200', 'selectedCurrency': '1', 'date': '07-03-2023', 'selectedBank': '1', 'bic': 'NWBKGB2L', 'iban': 'GB45NWBK60730152336905', 'accountNumber': '52336905', 'accountName': 'Lundy Investor ltd', 'reference': 'Josanik facility fee', 'interestCalculationToggle': 'false', 'offtakerRepaymentToggle': 'false','fundConvertedAmount': '127.2600','fundCurrencyExchangeRate': '1.2726','currencyConversionDate': '07-04-2023', 'CostDocuments': '[]', 'loanMappingList': '[{"selectedLoan":191,"loanMappingRatio":"20","loanMappingAmount":null},{"selectedLoan":291,"loanMappingRatio":"80","loanMappingAmount":null}]', 'clientId': '1', 'userId': '111', 'moduleId': '4', 'tabId': '34'}


        print(data)
        response = requests.request("POST", url, data=data)

        assert response.status_code == 200
        print(response.status_code)

    def test_add_cost_payment(self):
        url = url_2+'/add-payment'
        print(url)
        headers = {
        'content-type': "application/form-data",
        'cache-control': "no-cache",
        }   
        # data = {'selectedOfftaker':161,'selectedBorrower':52,'selectedCollateral':1,'contractNumber':'P1233adv45r','contractDate':'2021-08-01','totalQuantity':100,'selectedUnit':1,'deliveryMonth':'null','selectedPriceType':'null','price':'null','conversionRate':'null','finalPrice':'null','contractValue':'null','paymentTerms':'null','agent':'null','quality':'null','terms':'null','arbitration':'null','comments':'null','status':'null','selectedDetails':'offtaker contract','OfftakerContractDocuments':'null','clientId':1,'userId':1,'moduleId':12,'tabId':30,}
        data = {'selectedBorrower': '52', 'selectedFacility': '40', 'selectedCost': '1', 'amount_paid': '1002', 'selectedCurrency': '1', 'date': '07-03-2023', 'selectedBank': '1','selectedCostID':'181', 'bic': 'NWBKGB2L', 'iban': 'GB45NWBK60730152336905', 'accountNumber': '52336905', 'accountName': 'Lundy Investor ltd','fundConvertedAmount': '127.2600','fundCurrencyExchangeRate': '1.2726','currencyConversionDate': '07-04-2023', 'reference': 'Josanik facility fee', 'CostDocuments': '[]', 'clientId': '1', 'userId': '111', 'moduleId': '4', 'tabId': '36'}


        print(data)
        response = requests.request("POST", url, data=data)

        assert response.status_code == 200
        print(response.status_code)

    def test_get_cost_summary(self):
        url = url_2+'/cost-summary/172/744/06-06-2023/06-08-2023/null?clientId=1'
        print(url)
        headers = {
        'content-type': "application/json",
        'cache-control': "no-cache",
        }
        response = requests.request("GET", url, headers=headers)
        print(response)

        data = response.json()

        assert response.status_code == 200
        assert data['status'] == "success"
        print(data['status'])

        # Testing for fields
        fields1 = data['cost_summary']
        print(data['cost_summary'])
        # # fields1 = (fields['offtaker_contract_details'])
        assert type(fields1[0]['amount_paid']) == type(None)
        assert type(fields1[0]['borrower_id']) == int
        assert type(fields1[0]['borrower_name']) == str
        assert type(fields1[0]['currency_short_name']) == str
        assert type(fields1[0]['expense_amount']) == str
        assert type(fields1[0]['expense_date']) == str
        assert type(fields1[0]['facility_id']) == int
        assert type(fields1[0]['facility_registration_id']) == str
        assert type(fields1[0]['id']) == int
        assert type(fields1[0]['loan_expense_name']) == str
        assert type(fields1[0]['status']) == str
        assert type(data['start_date']) == str
        assert type(data['end_date']) == str


    def test_get_cost_overview(self):
        url = url_2+'/cost-overview/70?clientId=1'
        print(url)
        headers = {
        'content-type': "application/json",
        'cache-control': "no-cache",
        }
        response = requests.request("GET", url, headers=headers)
        print(response)

        data = response.json()

        assert response.status_code == 200
        assert data['status'] == "success"
        print(data['status'])


        # Testing for fields
        fields = data['cost_overview']
        print(data['cost_overview'])
        fields1 = (fields['facility_expense_transaction'])
        assert type(fields1[0]['account_name']) == str
        assert type(fields1[0]['borrower_id']) == int
        assert type(fields1[0]['borrower_name']) == str
        assert type(fields1[0]['currency_short_name']) == str
        assert type(fields1[0]['amount_paid']) == type(None)
        assert type(fields1[0]['account_number']) == int
        assert type(fields1[0]['bank_name']) == str
        assert type(fields1[0]['beneficiary_bank_id']) == int
        assert type(fields1[0]['bic']) == type(None)
        assert type(fields1[0]['expense_amount']) == float
        assert type(fields1[0]['expense_date']) == str
        assert type(fields1[0]['expense_id']) == int
        assert type(fields1[0]['facility_id']) == int
        assert type(fields1[0]['facility_registration_id']) == str
        assert type(fields1[0]['iban']) == type(None)
        assert (fields1[0]['id']) > 0
        assert type(fields1[0]['loan_expense_name']) == str
        assert type(fields1[0]['payment_date']) == type(None)
        assert type(fields1[0]['reference']) == str

        fields2 = list(fields['facility_transaction_document'])
        assert type(fields2[0]['document_path']) == str
        assert type(fields2[0]['display_file_name']) == str
        assert (fields2[0]['id']) > 0

        fields3 = list(fields['facility_transaction_loan_mapping'])
        assert type(fields3[0]['expense_amount']) == float
        assert type(fields3[0]['expense_ratio']) == float
        assert (fields3[0]['id']) > 0
        assert type(fields3[0]['loan_id']) == float
        assert type(fields3[0]['loan_registration_id']) == str

    def test_get_cost_payment_overview(self):
        url = url_2+'/cost-payment-overview/116?clientId=1'
        print(url)
        headers = {
        'content-type': "application/json",
        'cache-control': "no-cache",
        }
        response = requests.request("GET", url, headers=headers)
        print(response)

        data = response.json()

        assert response.status_code == 200
        assert data['status'] == "success"
        print(data['status'])


        # Testing for fields
        fields = data['cost_payment_overview']
        print(data['cost_payment_overview'])
        fields1 = (fields['facility_expense_payment_transaction'])
        assert type(fields1[0]['account_name']) == str
        assert type(fields1[0]['borrower_id']) == int
        assert type(fields1[0]['borrower_name']) == str
        assert type(fields1[0]['currency_short_name']) == str
        assert type(fields1[0]['amount_paid']) == str
        assert type(fields1[0]['account_number']) == int
        assert type(fields1[0]['bank_name']) == str
        assert type(fields1[0]['beneficiary_bank_id']) == int
        assert type(fields1[0]['bic']) == str
        assert type(fields1[0]['facility_id']) == int
        assert type(fields1[0]['facility_registration_id']) == str
        assert type(fields1[0]['iban']) == str
        assert (fields1[0]['id']) > 0
        assert type(fields1[0]['payment_date']) == str
        assert type(fields1[0]['reference']) == str
        assert type(fields1[0]['currency_rate']) == type(None)
        assert type(fields1[0]['converted_paid_amt']) == str
        assert type(fields1[0]['conversion_date']) == type(None)

        fields2 = (fields['facility_expense_payment_transaction_document'])
        assert type(fields2[0]['document_path']) == str
        assert type(fields2[0]['display_file_name']) == str
        assert type(fields2[0]['comments']) == type(None)
        assert (fields2[0]['id']) > 0

    def test_get_cost_payment_summary(self):
        url = url_2+'/cost-payment-summary/52/null/null/null/null/null/null?clientId=1'
        print(url)
        headers = {
        'content-type': "application/json",
        'cache-control': "no-cache",
        }
        response = requests.request("GET", url, headers=headers)
        print(response)

        data = response.json()

        assert response.status_code == 200
        assert data['status'] == "success"
        print(data['status'])


        # Testing for fields
        fields1 = data['cost_payment_summary']
        print(data['cost_payment_summary'])
        # # fields1 = (fields['offtaker_contract_details'])
        assert type(fields1[0]['amount_paid']) == str
        assert type(fields1[0]['borrower_id']) == int
        assert type(fields1[0]['currency_short_name']) == str
        assert type(fields1[0]['payment_date']) == str
        assert type(fields1[0]['facility_id']) == int
        assert type(fields1[0]['facility_registration_id']) == str
        assert type(fields1[0]['id']) == int
        assert type(fields1[0]['loan_expense_name']) == str
        # assert type(fields1[0]['start_date']) == str
        # assert type(fields1[0]['end_date']) == str
        assert type(fields1[0]['balance_amount']) == type(None)
        assert type(fields1[0]['converted_paid_amt']) == type(None)
        assert type(fields1[0]['currency_id']) == int
        assert type(fields1[0]['currency_rate']) == type(None)
        assert type(fields1[0]['expense_id']) == int
        assert type(fields1[0]['fund_currency_short_name']) == str
 


    def test_get_cost_payment_date_backcapping(self):
        url = url_2+'/cost-payment-date-backcapping/52/40/1/0?clientId=1'
        print(url)
        headers = {
        'content-type': "application/json",
        'cache-control': "no-cache",
        }
        response = requests.request("GET", url, headers=headers)
        print(response)

        data = response.json()

        assert response.status_code == 200
        assert data['status'] == "success"
        print(data['status'])


        # Testing for fields
        # # fields1 = (fields['offtaker_contract_details'])
        assert type(data['payment_date']) == str
        
    def test_get_currency_id(self):
        url = url_2+'/currency-id/41?clientId=1'
        print(url)
        headers = {
        'content-type': "application/json",
        'cache-control': "no-cache",
        }
        response = requests.request("GET", url, headers=headers)
        print(response)

        data = response.json()

        assert response.status_code == 200
        assert data['status'] == "success"
        print(data['status'])


        # Testing for fields
        fields1 = data['currency']
        print(data['currency'])
        assert type(fields1[0]['fund_currency_id']) == int

    def test_payment_trigger(self):
            url = url_2+'/payment-trigger/743/69/1/270?clientId=1'
            print(url)
            headers = {
            'content-type': "application/json",
            'cache-control': "no-cache",
            }
            response = requests.request("GET", url, headers=headers)
            print(response)

            data = response.json()

            assert response.status_code == 200
            assert data['status'] == "success"
            print(data['status'])