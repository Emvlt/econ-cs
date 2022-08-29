
import pyodbc 
import web_utils
import sql_utils
import constants


print('Connecting to server...')
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=6S3S0J3;'
                      'DATABASE=rightmove;'
                      'Trusted_Connection=yes;')
print('Creating cursor...')
cursor = conn.cursor()

def create_table(table_name = 'test'):
    if bool(sql_utils.query_table(cursor, 'test', 'table_exists', table_name)):
        sql_utils.query_table(cursor, 'modify', 'drop_table', table_name)

    sql_utils.query_table(cursor, 'modify', 'create_table', table_name)

    for feature_name in list(constants.FEATURES_OF_INTEREST.keys())+list(constants.EXTRA_FEATURES.keys()):
        sql_utils.query_table(cursor, 'modify', 'add_column', table_name, feature_name, constants.PYTHON_TO_SQL_TYPES[feature_name])

def populate_table(table_name = 'test', index = 0):
    query_string = f"https://www.rightmove.co.uk/property-for-sale/find.html?locationIdentifier=REGION%5E219&index={24*index}&propertyTypes=&includeSSTC=false&mustHave=&dontShow=&furnishTypes=&keywords="

    query_soup = web_utils.load_soup(query_string, 'query')

    properties_links = query_soup.find_all("a", {'class':"propertyCard-link" ,'data-test':"property-details"})
    for hyper_ref in properties_links:
        property_data = web_utils.get_property_data(property_key=f"https://www.rightmove.co.uk{hyper_ref.get('href')}")
        print(f"Processing property id {property_data['id']}")
        if not bool(sql_utils.query_table(cursor, 'test', 'is_in_table', table_name, property_data['id'])):
            sql_utils.query_table(cursor, 'modify', 'add_row', table_name, property_data)

if __name__=='__main__':
    create_table('properties')
    populate_table('properties', 0)