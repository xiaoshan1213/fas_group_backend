from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, Float, String, create_engine, Sequence, ForeignKey
from sqlalchemy.sql import select, and_
from app import Admin
from app import AdminGroup
from app import AdminJoinGroup
from app import ResGroup
from app import Namespace
from app import AdminToResGroup


engine = create_engine('mysql+pymysql://root:rootroot@127.0.0.1/fas')
conn = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()

adminJoinGroup = AdminJoinGroup()
admin = Admin()
adminGroup = AdminGroup()
resGroup = ResGroup()
namespace = Namespace()
admintoresgroup = AdminToResGroup()

st1 = select([admin.__table__]).where(
    and_(
        admin.__table__.c.name == 'wenjin',
        admin.__table__.c.customer_id == 0
        )
    )

st2 = adminGroup.__table__.select().where(
    and_(
        adminGroup.__table__.c.name == 'ns1',
        admin.__table__.c.customer_id == 0
    )   
)

res1 = conn.execute(st1)
res2 = conn.execute(st2)
row1 = res1.fetchone()
row2 = res2.fetchone()
# print("admin_id:", row1['id'], "; name:", row1['name'])
# print("group_id:", row2['id'])

st5 = adminJoinGroup.__table__.select().where(
    and_(
        adminJoinGroup.__table__.c.admin_id == row1['id'],
        adminJoinGroup.__table__.c.group_id == row2['id']
    )
)

res5 = session.query(AdminJoinGroup).filter_by(admin_id=row1['id'], group_id=row2['id']).first()
# res5 = conn.execute(st5)

if res5 == None:
    st3 = adminJoinGroup.__table__.insert().values(admin_id=row1['id'], group_id=row2['id'])
    conn.execute(st3)

st4 = adminJoinGroup.__table__.select()
res4 = conn.execute(st4)
row4 = res4.fetchone()
# print row4

# get all admin groups from current customer
session.query(AdminGroup).filter_by(customer_id=0)

# get all admin groups from current level admin user
# session.query(Admin).filter_by(name='wenjin')
# session.query(AdminJoinGroup).filter_by(admin_id=1)
# session.query(AdminGroup).filter_by(customer_id=0, id=1)

q = session.query(Admin, AdminGroup, AdminJoinGroup)\
.with_entities(AdminGroup.name)\
.filter(Admin.name == 'wenjin', Admin.customer_id == 0)\
.filter(Admin.id == AdminJoinGroup.admin_id)\
.filter(AdminJoinGroup.group_id == AdminGroup.id).all()
print q

# create admin group
adminGroup.__table__.insert().values(name='ns3', customer_id=0)

# create res group
resGroup.__table__.insert().values(name='rg3', customer_id=0)

# assgin admin users to that admin group
adminJoinGroup.__table__.insert().values(admin_id='', group_id='')

# assign namespaces to that res group (namespace already exists)
session.query(Namespace).filter_by(name='np1').first().update({'group_id' : 'res_group_id'})
session.commit()

# link admin group with res group
admintoresgroup.__table__.insert().values(admingroup_id='', resgroup_id='')

# get all namespaces for current level admin user



# print session.query(Admin).filter_by(name='sam').first()
session.close()
# engine.close()