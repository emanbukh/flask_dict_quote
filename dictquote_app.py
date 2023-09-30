from flask import Flask, render_template, request, redirect, url_for
import requests
import json 


dictquote_app=Flask(__name__)

def dictionary_api(keyword):
    """
    `dictionary_api` makes a request to a dictionary API and returns the JSON data for a
    given keyword.
     `dictionary_api` returns the data retrieved from the dictionary API for the
    given keyword.
    """
    word=requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en/{keyword}')
    word_data=word.json()
    return word_data

def quote_api(tag, limit):
    """
     `quote_api`makes a request to the PaperQuotes API to retrieve quotes based on a
    specified tag and limit.
    
    `quote_api` returns the `quotes_data` if the request is successful (status
    code 200). If there is an error, it prints the error message and returns `None`.
    """
    TOKEN = 'bbb2b83d42218ba52236a7a6df1b1b7460dae02c'
    PAPERQUOTES_API_ENDPOINT = f'https://api.paperquotes.com/apiv1/quotes/?tags={tag}&limit={limit}'
    headers = {'Authorization': f'TOKEN {TOKEN}'}

    quote = requests.get(PAPERQUOTES_API_ENDPOINT, headers=headers)

    if quote.status_code == requests.codes.ok:
        # Parse the JSON response
        quotes_data = quote.json()
        return quotes_data

    else:
        # Handle the error if the request was not successful
        print(f"Error: {quote.status_code} - {quote.text}")
        return None

def quote_day():

     """
     `quote_day()` function retrieves the quote of the day from the PaperQuotes API using an API
    token and returns the JSON response.
     `quote_day()` returns the JSON data received from the PaperQuotes API if the
    request is successful. 
    """
   
    TOKEN = 'bbb2b83d42218ba52236a7a6df1b1b7460dae02c'
    PAPERQUOTES_API_ENDPOINT = f'https://api.paperquotes.com/apiv1/qod/'
    headers = {'Authorization': f'TOKEN {TOKEN}'}

    qod = requests.get(PAPERQUOTES_API_ENDPOINT, headers=headers)

    if qod.status_code == requests.codes.ok:
       
        qod_data = qod.json()
        print(type(qod_data))
        print(qod_data)
        return qod_data

    else:
        # Handle the error if the request was not successful
        print(f"Error: {qod.status_code} - {qod.text}")
        return None





@dictquote_app.route('/', methods=['GET','POST']) #route to main page

  """
    This function handles a form submission, retrieves the user's name, and renders a template with the
    user's name as a parameter.
    either the rendered template 'result.html' with the user_name variable passed as an
    argument, or the rendered template 'form.html'.
    """

def form():
    if request.method == 'POST':
        # Get the user's name from the form submission
        user_name = request.form['user_name']
        return render_template('result.html', user_name=user_name)
    

    return render_template('form.html')



@dictquote_app.route('/words', methods=['GET','POST'])

 """
    a route in that handles GET and POST requests for a form.
    submission related to searching for words in a dictionary API.
    
    The code is returning a rendered template based on the conditions in the code. If the
    request method is 'POST' and the word_data is not empty, it returns the 'result_word.html' template
    with the user_input, word_word, word_meaning, word_meaning2, and word_meaning3 variables. 

    If the request method is not 'POST', it returns the 'form_word.html
    """

def form_word():
    try:
        if request.method == 'POST':
            # Get word that the user searched for from form submission
            user_input = request.form['user_input']

            word_data=dictionary_api(user_input)
            print(type(word_data)) #word_data type is dictionary
            print(word_data)
            if word_data !="":
            # This code block is checking if the `word_data` variable is not empty. If it is not
            # empty, it extracts specific information from the `word_data` dictionary and assigns it
            # to variables `word_word`, `word_meaning`, `word_meaning2`, and `word_meaning3`.
                word_word=word_data[0]['word']
                word_meaning=word_data[0]['meanings'][0]['definitions']
                word_meaning2=word_data[0]['meanings'][1]['definitions']
                word_meaning3=word_data[0]['meanings'][2]['definitions']
               
                return render_template('result_word.html',user_input=user_input, word_word=word_word, word_meaning=word_meaning, word_meaning2=word_meaning2,word_meaning3=word_meaning3)
        return render_template('form_word.html')
    except Exception as e:
        # Handle the exception gracefully (e.g., log the error, display an error message)
        error_message = f"An error occurred: {str(e)}"
        return render_template('error.html', error_message=error_message)



@dictquote_app.route('/quotes', methods=['GET','POST'])

 """
    `form_quote` is a route that handles both GET and POST requests
    to display a form for user input and fetch quotes using an API.

    The code is returning different templates based on the conditions. If the request method is
    POST and the quote_api function returns a non-empty result, it returns the 'result_quote.html'
    template with the user input and the fetched quotes. 

    If the quote_api function returns an empty result, it returns the 'error.html' template with an error message. If the request method is GET, it
    returns the '
    """

def form_quote():
    try:
        if request.method == 'POST':
            # Get the user's input from the form submission
            user_input = request.form['user_input']
            
            # Call the quote_api function to fetch quotes
            quotes_data = quote_api(user_input, limit=5)
            print(quotes_data)
            print(type(quotes_data)) #quotes_data type is dictionary
            quotes_save=[]

            if quotes_data !="":
                # Render the 'result_quote.html' template with the quotes_data
                for item in quotes_data.get('results', []):
                    quote = item.get('quote', '')  # Get the 'quote' value, default to empty string if not found
                    author = item.get('author', '')  # Get the 'author' value, default to empty string if not found
                    quotes_save.append({'quote': quote, 'author': author})

                return render_template('result_quote.html', user_input=user_input, quotes_save=quotes_save)
            else:
                # Handle the case where quote_api returned None (an error occurred)
                error_message = "An error occurred while fetching quotes."
                return render_template('error.html', error_message=error_message)

        # If it's a GET request, render the form
        return render_template('form_quote.html')

    except Exception as e:
        # Handle the exception gracefully (e.g., log the error, display an error message)
        error_message = f"An error occurred: {str(e)}"
        return render_template('error.html', error_message=error_message)

@dictquote_app.route('/quotes_day', methods=['GET','POST'])

"""
    handles both GET and POST requests to fetch and display the quote of the day.

    The code is returning either the rendered template 'form_qod.html' if the request method is
    GET, or the rendered template 'result_qod.html' 

    if the request method is POST and the quote of the
    day data is successfully fetched. 

    If there is an error while fetching the quote of the day, it
    returns the rendered template 'error.html' with an error message.
    """

def form_qod():
    try:
        if request.method == 'POST':
            # Get the user's input from the form submission
            
            # Call the quote_api function to fetch quotes
            qod_data = quote_day()
            print(qod_data)
            print(type(qod_data)) #quotes_data type is dictionary
            qod_save=[]

            if qod_data:
                # No need for a loop, as qod_data is a single dictionary, not a list
                quote = qod_data.get('quote', '')  # Get the 'quote' value, default to empty string if not found
                author = qod_data.get('author', '')  # Get the 'author' value, default to empty string if not found
                qod_save.append({'quote': quote, 'author': author})
                print(qod_save)

                return render_template('result_qod.html', qod_save=qod_save)
            else:
                 # Handle the case where fetching the quote failed
                 error_message = "An error occurred while fetching the quote of the day."
            return render_template('error.html', error_message=error_message)

        # If it's a GET request, render the form
        return render_template('form_qod.html')

    except Exception as e:
        # Handle the exception gracefully
        error_message = f"An error occurred: {str(e)}"
        return render_template('error.html', error_message=error_message)


# The `if __name__ == '__main__':` statement is used to check if the current script is being run
# directly or if it is being imported as a module.
if __name__ == '__main__':
    dictquote_app.run(debug=True)