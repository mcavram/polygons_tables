import core
import queries
import re
from mail import send_mail


oracle_db = core.connect_oracle('website', 'hainsley', '10.97.95.133', 'MAIN.PCA')

tables = oracle_db.execute(queries.table_query).fetchall()

final_query = ' '

ignore_tables = [
    'CT_FAIRFIELD_DUMMY_UNIVERSAL',
    'CT_LITCHFIELD_DUMMY_UNIVERSAL',
    'IN_DEARBORN_DUMMY_UNIVERSAL',
    'NJ_BERGEN_DUMMY_UNIVERSAL',
    'NJ_OCEAN_DUMMY_UNIVERSAL',
    'NJ_SOMERSET_DUMMY_UNIVERSAL',
    'NYC2_DUMMY_UNIVERSAL',
    'OH_GEAUGA_DUMMY_UNIVERSAL',
    'OH_PREBLE_DUMMY_UNIVERSAL',
    'OR_MULTNOMAH_DUMMY_UNIVERSAL',
    'VA_ALEXANDRIA_DUMMY_UNIVERSAL',
    'DC_UNIVERSAL',
    'SAN_FRANCISCO_UNIVERSAL', 
    'SEATTLE_UNIVERSAL',
    'NYC_UNIVERSAL',
    'NYC_UNIVERSAL_1702',
]

for data in tables:
    if data[0] not in ignore_tables:
        match = re.findall(r'(?P<state>\w{2})_(?P<county>.+_)', data[0])
        
        for state, county in match:
            table = 'PARCELS.{0}_{1}UNIVERSAL'.format(state,county)
            county = re.sub('_', ' ', county)
            county = re.sub(' $', '', county)
            final_query += queries.union_query.format(table, county, state)
           
final_query += queries.special_case_query
count_sum = oracle_db.execute(queries.count_query.format(final_query)).fetchone()

print('Total count: {0}'.format(count_sum[0]))

oracle_db.execute(queries.drop_backup_query)
oracle_db.execute(queries.create_backup_query)
oracle_db.execute(queries.drop_query)
oracle_db.execute(queries.create_query.format(final_query))
send_mail('scripts@propertyshark.com', 'cristina.avram@yardi.com','nina.chis@yardi.com, liviu.simioanca@yardi.com', 'PropertyShark - Matrix property shapes monthly update ',
'Hi, \n\nPropertyShark - Matrix property shapes monthly update is done.\n\n'
'The process runs from Jenkins every month and updates the table with property shapes for all counties.\n' 
)

