import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, Department as DepartmentModel, Employee as EmployeeModel, User as UserModel
from passlib.apps import custom_app_context as pwd_context
from sqlalchemy import Column, Integer, String


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

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    class Meta:
        model = UserModel


class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String()
        password = graphene.String()

    user = graphene.Field(lambda: User)
    ok = graphene.Boolean()

    def mutate(self, info, username, password):
        # if username is None or password is None:
            # abort(400)    # missing arguments
        # if User.query.filter_by(username=username).first() is not None:
            # abort(400)    # existing user
        user = UserModel(username=username)
        user.hash_password(password)
        ok = True
        db_session.add(user)
        db_session.commit()
        return CreateUser(user=user, ok=ok)

class Query(graphene.ObjectType):
    user = graphene.Field(User)
    departments = graphene.List(Department)
    employees = graphene.List(Employee)
    users = graphene.List(User)
    department = graphene.Field(Department,
                                id=graphene.String())

    def resolve_departments(self, info):
        query = Department.get_query(info)
        return query.all()

    def resolve_employees(self, info):
        query = Employee.get_query(info)
        return query.all()

    def resolve_users(self, info):
        query = User.get_query(info)
        return query.all()

    def resolve_department(self, info, id):
        query = Department.get_query(info)
        return query.all()

class Mutations(graphene.ObjectType):
    create_user = CreateUser.Field()

schema = graphene.Schema(query=Query, mutation=Mutations)
