db = db.getSiblingDB("wheather_app");
db.cities.drop()

db.cities.insertMany([
    {
        'location': 'Baniel',
        'max': 20,
        'min':4,
        'weather': 'Cubierto'
    },
    {
        'location': 'Madrid',
        'max': 22,
        'min':5,
        'weather': 'Nubes dispersas'
    }

])