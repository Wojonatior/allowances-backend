import graphene
from graphene import relay
from graphql import GraphQLError
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, Department as DepartmentModel, Employee as EmployeeModel, User as UserModel
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy import Column, Integer, String
from pprint import pprint


class Department(SQLAlchemyObjectType):
    id = graphene.ID()
    name = graphene.String()
    class Meta:
        model = DepartmentModel


class Employee(SQLAlchemyObjectType):
    id = graphene.ID()
    class Meta:
        model = EmployeeModel

class User(SQLAlchemyObjectType):
    id = graphene.ID()
    password_hash = graphene.String()
    class Meta:
        model = UserModel


class Login(graphene.Mutation):
    class Arguments:
        username = graphene.String()
        password = graphene.String()

    token = graphene.String()
    ok = graphene.Boolean()
    error = graphene.String()

    def mutate(self, info, username, password):
        user = User.get_query(info).filter_by(username=username).first()
        if user is None:
            return Login(token=None,  ok=False, error="Username does not exist")
        if not pwd_context.verify(password, user.password_hash):
            return Login(token=None,  ok=False, error="Password is invalid")
        
        return Login(token="sampleToken", ok=True, error=None)

class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String()
        password = graphene.String()

    user = graphene.Field(lambda: User)
    ok = graphene.Boolean()

    def mutate(self, info, username, password):
        ok = False

        if (username is None or password is None or
        len(username) is 0 or len(password) is 0):
            raise GraphQLError('username and password are required')
        if User.get_query(info).filter_by(username=username).first() is not None:
            raise GraphQLError('That username already exists')

        user = UserModel(username=username)
        user.hash_password(password)
        db_session.add(user)
        db_session.commit()
        ok = True
        return CreateUser(user=user, ok=ok)

class Query(graphene.ObjectType):
    node = graphene.relay.Node.Field()
    departments = graphene.List(Department)
    employees = graphene.List(Employee)
    users = graphene.List(User)
    department = graphene.Field(Department, id=graphene.ID())
    user = graphene.Field(User, id=graphene.ID())

    def resolve_user(self, info, id):
        query = User.get_query(info)
        return query.get(id)

    def resolve_department(self, info, id):
        query = Department.get_query(info)
        return query.get(id)

    def resolve_departments(self, info):
        query = Department.get_query(info)
        return query.all()

    def resolve_employees(self, info):
        query = Employee.get_query(info)
        return query.all()

    def resolve_users(self, info):
        query = User.get_query(info)
        return query.all()


class Mutations(graphene.ObjectType):
    create_user = CreateUser.Field()
    login = Login.Field()

schema = graphene.Schema(query=Query, mutation=Mutations)
