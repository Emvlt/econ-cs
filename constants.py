FEATURES_OF_INTEREST = {
    'id':int,
    'text':str,
    'prices':dict,
    'address':dict,
    'keyFeatures':list,
    'rooms':list,
    'bedrooms':int,
    'bathrooms':int,
}

IMAGES_FEATURES = [
    'images',
    'floorplans',
    'epcGraphs'
]

EXTRA_FEATURES = {
    'latitude' :float,
    'longitude':float,
    'pictures' :int,
    'price' :int,
}

PYTHON_TO_SQL_TYPES = {
    'id'         :'int',
    'text'       :'nvarchar(max)',
    'prices'     :'nvarchar(max)',
    'address'    :'nvarchar(max)',
    'keyFeatures':'nvarchar(max)',
    'rooms'      :'nvarchar(max)',
    'latitude'   :'float',
    'longitude'  :'float',
    'bedrooms'   :'int',
    'bathrooms'  :'int',
    'pictures'   :'int',
    'price'      :'int'
}