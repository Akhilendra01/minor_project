import Helpers
import json
import mysql.connector
import Utils

def generate(connection, client_addr):
    try: 
        data = Utils.generate_data()
        cursor = connection.cursor()
        sql = f"INSERT INTO users values('{client_addr[0]}', '{data['name'].strip()}', '{data['public_key']}')"
        try: 
            cursor.execute(sql)
            connection.commit()
            print('Entry done in database')                
            return json.dumps(data)
        except:
            return 'error in executing sql'
        
    except mysql.connector.Error as err:
        print("Error occurred while connecting to database:", err)
        return "An error has occured"
    
def get_pub_key(name, connection):
    if Utils.search(name, connection):
        public_key=Utils.get_public_key(name, connection)
        return public_key
    else:
        return "No such psedunym/ip exists"

def getnym(ip, connection):
    return Utils.getnym(ip, connection)

def getip(name, connection):
    return Utils.getip(name, connection)