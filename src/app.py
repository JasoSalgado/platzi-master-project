from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
from bson import json_util 
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_URI']= 'mongodb://localhost/pythonmongodb'
mongo = PyMongo(app)


@app.route('/entrepreneurs', methods=['POST'])
#Creating entrepreneurs
def create_entrepreneurs():
    #Receiving data
    entrepreneurs_name = request.json['entrepreneurs_name']
    entrepreneurs_lastname = request.json['entrepreneurs_lastname']
    entrepreneurs_company = request.json['entrepreneurs_company']
    entrepreneurs_type_company = request.json['entrepreneurs_type_company']
    entrepreneurs_country = request.json['entrepreneurs_country']

    if entrepreneurs_name and entrepreneurs_lastname and entrepreneurs_company and entrepreneurs_type_company:
        id = mongo.db.entrepreneurs.insert(
            {
                'entrepreneurs_name': entrepreneurs_name,
                'entrepreneurs_lastname': entrepreneurs_lastname,
                'entrepreneurs_company': entrepreneurs_company,
                'entrepreneurs_type_company': entrepreneurs_type_company,
                'entrepreneurs_country': entrepreneurs_country
            }
        )
        response = {
            'id': str(id),
            'entrepreneurs_name': entrepreneurs_name,
            'entrepreneurs_lastname': entrepreneurs_lastname,
            'entrepreneurs_company': entrepreneurs_company,
            'entrepreneurs_type_company': entrepreneurs_type_company,
            'entrepreneurs_country': entrepreneurs_country
        }
        return response
    else: 
        return not_found()

    


#Obtaining entrepreneurs
@app.route('/entrepreneurs', methods=['GET'])
def get_entrepreneurs():
    #Convert data from bson to json
    entrepreneurs = mongo.db.entrepreneurs.find()
    response = json_util.dumps(entrepreneurs)
    return Response(response, mimetype='application/json')


#Obtaining just one entrepreneur by id
@app.route('/entrepreneurs/<id>', methods=['GET'])
def get_entrepreneur(id):
    entrepreneur = mongo.db.entrepreneurs.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(entrepreneur)
    return Response(response, mimetype='application/json') 


#Delete entrepreneurs
@app.route('/entrepreneurs/<id>', methods=['DELETE'])
def delete_entrepreneur(id):
    mongo.db.entrepreneurs.delete_one({'_id': ObjectId(id)})
    response = jsonify({ 'message': 'Entrepreneur ' + id + ' was deleted successfully'})
    return response


#Update entrepreneurs
@app.route('/entrepreneurs/<id>', methods=['PUT'])
def update_entrepreneurs(id):
    entrepreneurs_name = request.json['entrepreneurs_name']
    entrepreneurs_lastname = request.json['entrepreneurs_lastname']
    entrepreneurs_company = request.json['entrepreneurs_company']
    entrepreneurs_type_company = request.json['entrepreneurs_type_company']
    entrepreneurs_country = request.json['entrepreneurs_country']

    if entrepreneurs_name and entrepreneurs_lastname and entrepreneurs_company and entrepreneurs_type_company:
        mongo.db.entrepreneurs.update_one({'_id': ObjectId(id)}, {'$set': {
            'entrepreneurs_name': entrepreneurs_name,
            'entrepreneurs_lastname': entrepreneurs_lastname,
            'entrepreneurs_company': entrepreneurs_company,
            'entrepreneurs_type_company': entrepreneurs_type_company,
            'entrepreneurs_country': entrepreneurs_country
        }})
        response = jsonify({ 'message': 'Entrepreneur ' + id + 'was updated successfully'})
        return response 


#Handling errors
@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message': 'Data not found' + request.url,
        'status': 404
    })
    response.status_code = 404
    
    return response
    

if __name__ == '__main__':
    app.run(debug=True)