from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
import mysql.connector

''' Server setings '''
app = Flask(__name__)
#CORS(app, support_credentials=True)

#!!!!!!!!!!!!!!!
mySqlHost = "";
mySqlUser = "";
mySqlPass = "";
mySqlDataBase = "";



def do_insert(in_date, username, last_name, first_name, chat_type, chat_id, queryText):
    mydb = mysql.connector.connect(
        host=mySqlHost,
        user=mySqlUser,
        passwd=mySqlPass,
        database=mySqlDataBase,
        autocommit=True
    )
    mycursor = mydb.cursor()

    sSql = r" INSERT INTO "
    sSql += r"`tg_bigdata`(`date`, `username`, `last_name`, `first_name`, `chat_type`, `chat_id`, `queryText`, `source`)"
    sSql += r" VALUES( '" + str(in_date) + "', '" + str(username) + "', '" + str(last_name) + "', '" + str(first_name) + "', "
    sSql += r" '" + str(chat_type) + "', '" + str(chat_id) + "', '" + str( queryText )+ "', 'TG')"
    mycursor.execute(sSql)


@app.route('/api/tg/jonny/', methods=['POST', 'GET', 'OPTIONS'])
def add_message():
    data = request.json
    queryResult = data['queryResult']
    queryText = queryResult['queryText']
    originalDetectIntentRequest = data['originalDetectIntentRequest']
    payload_data = originalDetectIntentRequest['payload']['data']
    chat = payload_data['chat']
    date = payload_data['date']
    msg_from = payload_data['from']
    chat_type = chat['type']
    chat_id = chat['id']
    last_name = ''
    try:
        last_name = msg_from['last_name']
    except:
        pass
    first_name = ''
    try:
        first_name = msg_from['first_name']
    except:
        pass
    username = ''
    try:
        username = msg_from['username']
    except:
        pass
    do_insert(date, username, last_name, first_name, chat_type, chat_id, queryText)
    return 'OK'


if __name__ == "__main__":
    app.run()
