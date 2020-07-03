# 导入:
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
#import sqlalchemy

# 初始化数据库连接:
engine = create_engine('mysql://root:abc123@localhost:3306/test?charset=uft8')

# 创建对象的基类:
Base = declarative_base()

# 定义User对象:
class User(Base):
    # 表的名字:
    __tablename__ = 'user'

    # 表的结构:
    id = Column(String(20), primary_key=True)
    name = Column(String(20))

    def __init__(self, id, name):
        self.id = id
        self.name = name
        #self.email = email  

Base.metadata.create_all(engine)


# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

def create_db():
    # 创建session对象:
    session = DBSession()
    # 创建新User对象:
    new_user = User(id='6', name='haha')
    # 添加到session:
    session.add(new_user)
    # 提交即保存到数据库:
    session.commit()
    session.close()

def query_db():  
    session = DBSession()

    # 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
    user = session.query(User).filter(User.id=='6').one()
    # 打印类型和对象的name属性:
    print('type:', type(user))
    print('name:', user.name)
    # 关闭Session:
    session.close()

def main():
    create_db()
    query_db()

main()