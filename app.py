from flask import Flask
from flask_restful import Resource, Api, reqparse
import random
import mysql.connector as mariadb
import pandas as pd

#Database connection
mariadb_connection = mariadb.connect(user='root', password='', database='taxiapp', host='127.0.0.1', port='3306')
cursor = mariadb_connection.cursor()

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
class nearby(Resource):
    #define get for nearby
    def get(self):
        data = "lat"
        lat = random.randrange(-100, 110)
        long = random.randrange(-100, 110)
        lat1 = random.randrange(-180, 110)
        long1 = random.randrange(-180, 110)
        lat2 = random.randrange(-135, 110)
        long2 = random.randrange(-135, 110)
        lat3 = random.randrange(-165, 110)
        long3 = random.randrange(-165, 110)
        taxidriver = ["taxi1","taxi2"]
        return {'tax1':{
            'latitud': lat,
            'longitud': long },
                'tax2':{
            'latitud': lat1,
            'longitud': long1 },
                'tax3':{
            'latitud': lat2,
            'longitud': long2 },
                'tax4':{
            'latitud': lat3,
            'longitud': long3 },

            }
class bookings(Resource):
    #define get for bookings
    def get(self, user_id):

        return {'Bookings':"list bookkings"}

class cab_history(Resource):
    # define get for nearby
    def get(self, user_id):
        arraym = pd.read_sql("SELECT user_bookings, user FROM members WHERE id = %s", con=mariadb_connection, params=(user_id))
        user = []

        for i, v in arraym.iterrows():
            user.append(
                {'userid': "{}".format(v['id']), 'username': "{}".format(v['user']),
                 'booking_history': "{}".format(v['user_bookings'])})

        return {'user': "{}".format(user)}

class userid(Resource):
    # define get for nearby
    def get(self,user_id):
        arraym = pd.read_sql("SELECT * FROM members WHERE id = %s", con=mariadb_connection, params=(user_id))
        user = []

        for i,v in arraym.iterrows():
            user.append({'userid': "{}".format(v['id']), 'username':"{}".format(v['user']), 'email':"{}".format(v['email']), 'balance':"{}".format(v['balance']), 'booking_history': "{}".format(v['user_bookings'])})

        return {'user': "{}".format(user)}

class user(Resource):
    # define get for nearby
    def get(self):
        arraym = pd.read_sql("SELECT * FROM members", con=mariadb_connection)
        user = []
        for index, values in arraym.iterrows():
            user.append({'username': "{}".format(values['user']),'email': "{}".format(values['email'])})
        return {'users': "{}".format(user)}


class create_user(Resource):
    # define post for creating user
    def post(self):
        parser.add_argument('username', type=str)
        parser.add_argument('email', type=str)
        args = parser.parse_args()
        cursor.execute("INSERT INTO members (user,email) VALUES (%s,%s)",(args['username'], args['email']))
        mariadb_connection.commit()


        return {
            'username': "{}".format(args['username']),
            'email': "{}".format(args['email'])
        }


class bookCab(Resource):
    # define post for creating user
    def post(self):
        parser.add_argument('username', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('Source', type=str)
        parser.add_argument('Destination', type=str)
        args = parser.parse_args()
        cursor.execute("INSERT INTO members (user,email) VALUES (%s,%s)",(args['username'], args['email']))
        cursor.execute("INSERT INTO members (user_bookings) )
        mariadb_connection.commit()


        return {
            'username': "{}".format(args['username']),
            'email': "{}".format(args['email'])
        }


api.add_resource(nearby, '/nearby')

api.add_resource(cab_history, '/user/<user_id>/bookings')

# api.add_resource(cab_history, '/cab_history')

api.add_resource(userid, '/user/<user_id>')

api.add_resource(user, '/alluser')

api.add_resource(create_user, '/create_user')


if __name__ == '__main__':
    app.run(debug=True)