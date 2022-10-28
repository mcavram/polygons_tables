table_query = """
    SELECT distinct TABLE_NAME
    FROM ALL_TAB_COLUMNS
    WHERE owner like '%PARCELS%'
        and TABLE_NAME like '%UNIVERSAL%'
        and column_name like 'PROPKEY' 
"""


union_query = """
    select a.marketid, a.propertyid, a.propkey, a.county, a.state, b.geo, c.propertystatus
    from pi_ei.propkey_match a 
        join {0} b on a.propkey = b.propkey
        join pi_ei.market_export c 
        on a.marketid = c.marketid and a.propertyid = c.propertyid
    where a.county = '{1}' and a.state = '{2}' and b.propkey != 0
    
    union all
"""
drop_backup_query = """
    drop table pi_ei.backup_ps_polygons_2020
"""

create_backup_query = """
    create table pi_ei.backup_ps_polygons_2020 as (select * from pi_ei.ps_polygons_2020)
"""

drop_query = """
    drop table pi_ei.ps_polygons_2020
"""

create_query = """
    create table pi_ei.ps_polygons_2020
    as (
        {0}
    )

"""

special_case_query = """
    select  a.marketid, a.propertyid, a.propkey, a.county, a.state, b.geo, c.propertystatus
        from pi_ei.propkey_match a 
            join PARCELS.SAN_FRANCISCO_UNIVERSAL b on a.propkey = b.propkey 
            join pi_ei.market_export c 
            on a.marketid = c.marketid and a.propertyid = c.propertyid
        where a.county = 'SAN FRANCISCO' and a.state = 'CA' and b.propkey != 0
    
    union all
    
    select a.marketid, a.propertyid, a.propkey, a.county, a.state, b.geo, c.propertystatus
    from pi_ei.propkey_match a 
        join PARCELS.SEATTLE_UNIVERSAL b on a.propkey = b.propkey 
        join pi_ei.market_export c 
        on a.marketid = c.marketid and a.propertyid = c.propertyid
    where a.county = 'SEATTLE' and a.state = 'WA' and b.propkey != 0
    
    union all
    
    select a.marketid, a.propertyid, a.propkey, a.county, a.state, b.geo, c.propertystatus
    from pi_ei.propkey_match a 
        join PARCELS.NYC2_UNIVERSAL b on a.propkey = b.propkey 
        join pi_ei.market_export c 
        on a.marketid = c.marketid and a.propertyid = c.propertyid
    where a.county = 'New York' and a.state = 'NY' and b.propkey != 0
            
    union all
            
    select a.marketid, a.propertyid, a.propkey, a.county, a.state, b.geo, c.propertystatus
    from pi_ei.propkey_match a 
        join PARCELS.DC_UNIVERSAL b on a.propkey = b.propkey 
        join pi_ei.market_export c 
        on a.marketid = c.marketid and a.propertyid = c.propertyid   
    where a.county = 'District of Columbia' and a.state = 'DC' and b.propkey != 0
"""

count_query = """
    select  count(*)
    from (
        {0}
    ) x
"""
