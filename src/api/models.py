""" Module handling database connection. 

Plan is to use Tortoise ORM for handling data 
connection.
"""

# standard imports

# third-party imports
from tortoise import fields, models, Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from passlib.hash import bcrypt

# internal imports

class Users(models.Model):
    """ User model. """

    id = fields.IntField(pk=True)
    username= fields.CharField(max_length=100, unique=True)
    hashed_password = fields.CharField(max_length=255)
    email = fields.CharField(max_length=100, unique=True)
    is_logged_in = fields.BooleanField(default=False)
    last_logged_date = fields.DatetimeField(auto_now=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    def verify_password(self, password: str):
        return bcrypt.verify(password, self.hashed_password)

user_pydantic = pydantic_model_creator(Users, name="user")
userin_pydantic = pydantic_model_creator(Users, name="userin", 
    include=('username', 'hashed_password', 'email'))
user_token_pydantic = pydantic_model_creator(Users, name="user_token",
    include=('username', 'id', 'email'))

class TimeseriesData(models.Model):
    """ Time series data model. """

    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.Users')
    start_date = fields.DatetimeField()
    end_date = fields.DatetimeField()
    resolution_min = fields.DecimalField(max_digits=7, decimal_places=3)
    created_at = fields.DatetimeField(auto_now_add=True)
    name = fields.CharField(max_length=100)
    description = fields.CharField(max_length=255)
    image = fields.CharField(max_length=100)
    filename = fields.CharField(max_length=100)
    category = fields.CharField(max_length=100)


ts_minimal= pydantic_model_creator(TimeseriesData,
name="ts_full_minimal", include=('name', 'filename', 'category'))

class ScenarioMetadata(models.Model):
    """ Scenario metadata model. """

    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.Users')
    created_at = fields.DatetimeField(auto_now_add=True)
    name = fields.CharField(max_length=100)
    description = fields.CharField(max_length=255)
    solar = fields.BooleanField()
    ev = fields.BooleanField()
    storage = fields.BooleanField()
    filename = fields.CharField(max_length=100)


class ReportMetadata(models.Model):
    """ Report metadata model. """

    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.Users')
    created_at = fields.DatetimeField(auto_now_add=True)
    name = fields.CharField(max_length=100)
    description = fields.CharField(max_length=255)
    status = fields.CharField(max_length=100)
    scenario_name = fields.CharField(max_length=100)
    report_file = fields.CharField(max_length=100)
    report_data_file = fields.CharField(max_length=100)


class Labels(models.Model):
    """ Labels model. """

    id = fields.IntField(pk=True)
    labelname = fields.CharField(max_length=100)
    user = fields.ForeignKeyField('models.Users')
    created_at = fields.DatetimeField(auto_now_add=True)

class ScenarioLabels(models.Model):
    """ Scenario label model. """
    
    id = fields.IntField(pk=True)
    scenario_id = fields.IntField()
    user = fields.ForeignKeyField('models.Users')
    created_at = fields.DatetimeField(auto_now_add=True)
    labelname = fields.CharField(max_length=100)

class ReportLabels(models.Model):
    """ Report labels model ."""

    id = fields.IntField(pk=True)
    report_id = fields.IntField()
    user = fields.ForeignKeyField('models.Users')
    created_at = fields.DatetimeField(auto_now_add=True)
    labelname = fields.CharField(max_length=100)

class DataComments(models.Model):
    """ Report labels model ."""

    id = fields.IntField(pk=True)
    timeseriesdata = fields.ForeignKeyField('models.TimeseriesData')
    comment = fields.CharField(max_length=1000)
    edited = fields.BooleanField()
    user = fields.ForeignKeyField('models.Users', related_name='user')
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

data_comments_pydantic = pydantic_model_creator(DataComments,
name="data_comment", include=("id", "comment", "user.username"))

class UserSharedTimeSeriesData(models.Model):
    """ Time series data shared with users """

    id = fields.IntField(pk=True)
    timeseries_data = fields.ForeignKeyField('models.TimeseriesData')
    user = fields.ForeignKeyField('models.Users')
    shared_date = fields.DatetimeField(auto_now_add=True)

    class Meta:
        unique_together=(("timeseries_data", "user"), )

user_shared_ts_data_pydantic = pydantic_model_creator(
    UserSharedTimeSeriesData, name="usr_shr_ts_data"
)

Tortoise.init_models(["models"], "models")


ts_pydantic = pydantic_model_creator(TimeseriesData,
name="ts_full")

if __name__ == '__main__':
    pass