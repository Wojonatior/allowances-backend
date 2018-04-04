import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, Department as DepartmentModel, Employee as EmployeeModel, User as UserModel


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
    class Meta:
        model = UserModel

class Query(graphene.ObjectType):
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


schema = graphene.Schema(query=Query)
