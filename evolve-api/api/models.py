""" Module handling database connection. 

Plan is to use Tortoise ORM for handling data 
connection.
"""

# standard imports

# third-party imports
from tortoise import fields
import tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from passlib.hash import bcrypt

# internal imports


class Users(tortoise.models.Model):
    """User model."""

    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=100, unique=True)
    hashed_password = fields.CharField(max_length=255)
    email = fields.CharField(max_length=100, unique=True)
    is_logged_in = fields.BooleanField(default=False)
    last_logged_date = fields.DatetimeField(auto_now=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    def verify_password(self, password: str) -> bool:
        """ Method to verify password. """
        return bcrypt.verify(password, self.hashed_password)


user_pydantic = pydantic_model_creator(Users, name="user")
userin_pydantic = pydantic_model_creator(
    Users, name="userin", include=("username", "hashed_password", "email")
)
user_token_pydantic = pydantic_model_creator(
    Users, name="user_token", include=("username", "id", "email")
)


class UserSharedTimeSeriesData(tortoise.models.Model):
    """Time series data shared with users"""

    id = fields.IntField(pk=True)
    timeseriesdata = fields.ForeignKeyField(
        "models.TimeseriesData", related_name="usr_shared_data"
    )
    user = fields.ForeignKeyField("models.Users")
    shared_date = fields.DatetimeField(auto_now_add=True)

    class Meta:
        unique_together = (("timeseriesdata", "user"),)


user_shared_ts_data_pydantic = pydantic_model_creator(
    UserSharedTimeSeriesData, name="usr_shr_ts_data"
)


class TimeseriesData(tortoise.models.Model):
    """Time series data model."""

    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.Users")
    start_date = fields.DatetimeField()
    end_date = fields.DatetimeField()
    resolution_min = fields.DecimalField(max_digits=7, decimal_places=3)
    created_at = fields.DatetimeField(auto_now_add=True)
    name = fields.CharField(max_length=100)
    description = fields.CharField(max_length=255)
    image = fields.CharField(max_length=100)
    filename = fields.CharField(max_length=100)
    category = fields.CharField(max_length=100)
    usr_shared_data: fields.ReverseRelation["UserSharedTimeSeriesData"]


ts_minimal = pydantic_model_creator(
    TimeseriesData, name="ts_full_minimal", include=("name", "filename", "category")
)
ts_pydantic = pydantic_model_creator(TimeseriesData, name="ts_full")


class ScenarioLabels(tortoise.models.Model):
    """Scenario label model."""

    id = fields.IntField(pk=True)
    scenario = fields.ForeignKeyField(
        "models.ScenarioMetadata", related_name="scen_meta"
    )
    user = fields.ForeignKeyField("models.Users")
    created_at = fields.DatetimeField(auto_now_add=True)
    label = fields.ForeignKeyField("models.Labels")


scen_label_pydantic = pydantic_model_creator(ScenarioLabels, name="scen_label_full")


class ScenarioMetadata(tortoise.models.Model):
    """Scenario metadata model."""

    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.Users")
    created_at = fields.DatetimeField(auto_now_add=True)
    name = fields.CharField(max_length=100)
    description = fields.CharField(max_length=255)
    solar = fields.BooleanField()
    ev = fields.BooleanField()
    storage = fields.BooleanField()
    filename = fields.CharField(max_length=100)
    scen_meta: fields.ReverseRelation["ScenarioLabels"]


scenmeta_pydantic = pydantic_model_creator(ScenarioMetadata, name="scen_full")


class ReportMetadata(tortoise.models.Model):
    """Report metadata model."""

    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.Users")
    created_at = fields.DatetimeField(auto_now_add=True)
    name = fields.CharField(max_length=100)
    description = fields.CharField(max_length=255)
    status = fields.CharField(max_length=100)
    scenario = fields.ForeignKeyField("models.ScenarioMetadata")


report_pydantic = pydantic_model_creator(ReportMetadata, name="report_full")


class Labels(tortoise.models.Model):
    """Labels model."""

    id = fields.IntField(pk=True)
    labelname = fields.CharField(max_length=100)
    description = fields.CharField(max_length=1000)
    user = fields.ForeignKeyField("models.Users")
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        unique_together = (("labelname", "user"),)


label_pydantic = pydantic_model_creator(Labels, name="label_full")


class Notifications(tortoise.models.Model):
    """Notification model."""

    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.Users")
    created_at = fields.DatetimeField(auto_now_add=True)
    message = fields.TextField()
    archived = fields.BooleanField()
    visited = fields.BooleanField()


notification_pydantic = pydantic_model_creator(Notifications, name="notification_full")


class DataComments(tortoise.models.Model):
    """Report labels model ."""

    id = fields.IntField(pk=True)
    timeseriesdata = fields.ForeignKeyField("models.TimeseriesData")
    comment = fields.CharField(max_length=1000)
    edited = fields.BooleanField()
    user = fields.ForeignKeyField("models.Users", related_name="user")
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)


data_comments_pydantic = pydantic_model_creator(
    DataComments, name="data_comment", include=("id", "comment", "user.username")
)


# Tortoise.init_models(["models"], "models")


if __name__ == "__main__":
    pass
