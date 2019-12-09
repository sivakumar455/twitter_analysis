#!/Users/sivakumarpadala/anaconda3/envs/tensorflow_env/bin/python
import twitter_app as twt_api
import nlp as nlp

from flask import render_template, request, jsonify
from flask import Flask

app = Flask(__name__)

# index webpage displays cool visuals and receives user input text for model
@app.route('/')
@app.route('/index')
def index():

    # render web page with plotly graphs
    return render_template('master.html')

# web page that handles user query and displays model results
@app.route('/go')
def go():
    # save user input in query
    query = request.args.get('query', '')
    #print(query)

    api = twt_api.create_api()
    tweet_list, tweet_text = twt_api.search_tweet(api, query)
    
    # Use NLP to process tweet text

    # This will render the go.html Please see that file.
    return render_template(
        'go.html',
        query=query,
        tweet_list = tweet_list,
        tweet_text = tweet_text
    )

app.run(host='localhost', port=3001, debug=True)
