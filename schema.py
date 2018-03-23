import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from models import db_session, Department as DepartmentModel, Employee as EmployeeModel, User as UserModel


class Department(SQLAlchemyObjectType):
    class Meta:
        model = DepartmentModel


class Employee(SQLAlchemyObjectType):
    class Meta:
        model = EmployeeModel

class User(SQLAlchemyObjectType):
    class Meta:
        model = UserModel

class Query(graphene.ObjectType):
    departments = graphene.List(Department)
    employees = graphene.List(Employee)
    users = graphene.List(User)

    def resolve_departments(self, info):
        query = Department.get_query(info)
        return query.all()

    def resolve_employee(self, info):
        query = Employee.get_query(info)
        return query.all()

    def resolve_users(self, info):
        query = User.get_query(info)
        return query.all()
    


schema = graphene.Schema(query=Query)
