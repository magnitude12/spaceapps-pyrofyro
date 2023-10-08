import math
from twilio.rest import Client
import csv
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


cred = credentials.Certificate("path/to/your/firebase/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def fetch_data_from_firestore():
    data = []
    collection_ref = db.collection("userdetails")
    docs = collection_ref.stream()

    for doc in docs:
        doc_data = doc.to_dict()
        data.append(doc_data)

    return data

firebase_data = fetch_data_from_firestore()


def fetch_data_from_csv(csv_file):
    data = []
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)

    return data

csv_file = "wildfire.csv"
csv_data = fetch_data_from_csv(csv_file)

def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    radius_earth = 6371.0
    distance = radius_earth * c
    
    return distance

account_sid = "SK7fb619c685e593697b3e22c047a6c7dc"
auth_token = "9fb16b1db104c34e7e8d3532b31f4ae4"
client = Client(account_sid, auth_token)

def send_sms(phone_number, message):
    try:
        message = client.messages.create(
            body=message,
            from_="your_twilio_number",
            to=phone_number
        )
        print(f"Message sent to {phone_number}: {message.sid}")
    except Exception as e:
        print(f"Error sending message: {str(e)}")


for person in firebase_data:
    person_lat = float(person['lat'])
    person_long = float(person['long'])
    person_phone = person['phone']
    uname = person['uname']

    for wildfire in csv_data:
        wildfire_lat = float(wildfire['latitude'])
        wildfire_long = float(wildfire['longitude'])
        if __name__ == "__main__":
            lat1 = person_lat
            lon1 = person_long
            lat2 = wildfire_lat
            lon2 = wildfire_long
    
            distance = haversine(lat1, lon1, lat2, lon2)

        if distance <= 3:
            message = f"Hello {uname}, there is a wildfire near your location. Stay safe!"
            send_sms(person_phone, message)

#####this is run as a cron job 