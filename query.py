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

q1 = session.query(Admin, AdminGroup, AdminJoinGroup)\
.with_entities(AdminGroup.id)\
.filter(Admin.name == 'wenjin', Admin.customer_id == 0)\
.filter(Admin.id == AdminJoinGroup.admin_id)\
.filter(AdminJoinGroup.group_id == AdminGroup.id).all()
# print q1

# get all namespaces for current level admin user
list1 = [value for (value,) in q1]
print list1
res = conn.execute(admintoresgroup.__table__.select().where(admintoresgroup.__table__.c.admingroup_id.in_(list1)))
result = [r[1] for r in res]
print result
res = conn.execute(namespace.__table__.select().where(namespace.__table__.c.group_id.in_(result)))
result = [r[1] for r in res]
print result

# if current level is global
# direct query namespace of current customer_id for all namespaces
session.query(Namespace).filter_by(customer_id=0).all()

# create admin group
adminGroup.__table__.insert().values(name='ns3', customer_id=0)

# create res group
resGroup.__table__.insert().values(name='rg3', customer_id=0)

# assgin admin users to that admin group
adminJoinGroup.__table__.insert().values(admin_id='', group_id='')

# assign namespaces to that res group (namespace already exists)
session.query(Namespace).filter_by(name='np1').update({'group_id' : 0})
# session.commit()

# link admin group with res group
ag1 = session.query(AdminGroup).filter_by(name='ns1').first()
rg1 = session.query(ResGroup).filter_by(name='rg1').first()
# rg1 = session.query(ResGroup).first()
# conn.execute(admintoresgroup.__table__.insert().values(admingroup_id=ag1.id, resgroup_id=rg1.id))

ag2 = session.query(AdminGroup).filter_by(name='ns2').first()
rg2 = session.query(ResGroup).filter_by(name='rg2').first()
# conn.execute(admintoresgroup.__table__.insert().values(admingroup_id=ag2.id, resgroup_id=rg2.id))

# print q2

# log?

# auth client (filter by namespace_id)

# user (filter by namespace_id)

print q2


# print session.query(Admin).filter_by(name='sam').first()
session.close()
# engine.close()