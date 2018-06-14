from sqlalchemy import Column, Integer, Float, String, create_engine, Sequence, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('mysql+pymysql://root:rootroot@127.0.0.1/fas')
Base = declarative_base()

class Admin(Base):
    __tablename__ = 'admins'
    id = Column(Float, Sequence('admin_id_seq'), primary_key=True)
    name = Column(String(50))
    customer_id = Column(Float, nullable=False)

class AdminGroup(Base):
    __tablename__ = 'admingroups'
    id = Column(Float, Sequence('admin_group_id_seq'), primary_key=True)
    name = Column(String(36), nullable=False)
    customer_id = Column(Float, nullable=False)

class AdminJoinGroup(Base):
    __tablename__ = 'adminjoingroups'
    id = Column(Integer, primary_key=True, default=0, autoincrement=True)
    admin_id = Column(ForeignKey('admins.id', ondelete='CASCADE'), nullable=False, primary_key=False)
    group_id = Column(ForeignKey('admingroups.id', ondelete='CASCADE'), nullable=False, primary_key=False)

class Namespace(Base):
    __tablename__ = 'namespaces'
    id = Column(Integer, primary_key=True, default=0, autoincrement=True)
    name = Column(String(36), nullable=False)
    customer_id = Column(Float, nullable=False)
    group_id = Column(Float, nullable=True)

class ResGroup(Base):
    __tablename__ = 'resgroups'
    id = Column(Integer, primary_key=True, default=0, autoincrement=True)
    name = Column(String(36), nullable=False)
    customer_id = Column(Float, nullable=False)

class AdminToResGroup(Base):
    __tablename__ = 'admintoresgroups'
    admingroup_id = Column(ForeignKey('admingroups.id', ondelete='CASCADE'), nullable=False, primary_key=True)
    resgroup_id = Column(ForeignKey('resgroups.id', ondelete='CASCADE'), nullable=False, primary_key=False)


# AdminJoinGroup.__table__.drop(engine)
# Base.metadata.create_all(engine)
# AdminJoinGroup.__table__.create(engine)
# Namespace.__table__.create(engine)
# ResGroup.__table__.create(engine)
# AdminToResGroup.__table__.create(engine)
# engine.close()
# ed_user = Admin(name='ed')
# session.add(ed_user)
# session.commit()
# our_user = session.query(Admin).filter_by(name='ed').first()
# print our_user
