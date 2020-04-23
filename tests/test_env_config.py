import os

import mock
import pytest

import envorm as orm


@pytest.fixture
def set_base_env(request):

    values = (
        ("STRING_EXAMPLE", "Result"),
        ("INT_EXAMPLE", "1"),
        ("FLOAT_EXAMPLE", "1.1"),
        ("BOOLEAN_EXAMPLE", "true"),
        ("LIST_EXAMPLE_SINGLE", "Result"),
        ("LIST_EXAMPLE_MULTIPLE", "1,2,3"),
    )
    for key, value in values:
        os.environ[key] = value

    def finalizer():
        for key, value in values:
            if key in os.environ:
                del os.environ[key]
            os.unsetenv(key)

    request.addfinalizer(finalizer=finalizer)


class TestBaseField(object):

    def test_should_get_string_value(self, set_base_env):
        model = orm.BaseField("STRING_EXAMPLE")
        assert model.value == "Result"

    def test_should_got_none_if_not_set(self, set_base_env):
        model = orm.BaseField("ENV_DOES_NOT_EXIST_")
        assert model.value is None

    def test_should_default_value_works(self, set_base_env):
        model = orm.BaseField("ENV_DOES_NOT_EXIST_", "Hi")
        assert model.value == "Hi"

    def test_should_value_cache_works(self, set_base_env):
        field_name = "STRING_EXAMPLE"

        model = orm.BaseField(field_name)

        with mock.patch.object(model, "_get_value") as mocked_update:
            mocked_update.return_value = "Hi"
            value = model.value
            value = model.value
            value = model.value
        assert value == "Hi"
        assert mocked_update.call_count == 1

    def test_should_raise_error_if_value_is_bad(self, set_base_env):

        class NewField(orm.BaseField):

            type_name = "new_field"

            def convert(self, value):
                if value == "Result":
                    self.raise_error(value)
                return value

        field_name = "STRING_EXAMPLE"

        model = NewField(field_name)

        with pytest.raises(orm.ConvertError) as exception:
            model.value
        assert exception.value.name == field_name
        assert exception.value.raw_value == "Result"
        assert exception.value.expected_type == "new_field"

    def test_should_raise_error_if_value_is_required(self, set_base_env):

        class NewField(orm.BaseField):

            type_name = "new_field"

        field_name = "ENV_DOES_NOT_EXIST"

        model = NewField(field_name, required=True)

        with pytest.raises(orm.ValueRequired) as exception:
            model.value
        assert exception.value.name == field_name

    def test_should_update_raise_error_if_value_is_bad(self, set_base_env):
        class NewField(orm.BaseField):
            type_name = "new_field"

            def convert(self, value):
                self.raise_error(value)

        field_name = "STRING_EXAMPLE"

        model = NewField(field_name)

        with pytest.raises(orm.ConvertError) as exception:
            model.update()
        assert exception.value.name == field_name
        assert exception.value.raw_value == "Result"
        assert exception.value.expected_type == "new_field"


def test_should_string_field_works(set_base_env):
    model = orm.StringField("STRING_EXAMPLE")
    assert model.value == "Result"


def test_should_string_field_choices_validation(set_base_env):
    field = orm.StringField("STRING_EXAMPLE", choices=["field-value"])
    with pytest.raises(orm.ValidationError):
        field.validate()


class TestIntField(object):
    def test_should_non_int_raise_error(self, set_base_env):
        model = orm.IntField("STRING_EXAMPLE")
        with pytest.raises(orm.ConvertError):
            model.value

    def test_should_return_int(self, set_base_env):
        model = orm.IntField("INT_EXAMPLE")
        assert isinstance(model.value, int)


class TestFloatField(object):
    def test_should_non_int_raise_error(self, set_base_env):
        model = orm.FloatField("STRING_EXAMPLE")
        with pytest.raises(orm.ConvertError):
            model.value

    def test_should_return_int(self, set_base_env):
        model = orm.FloatField("FLOAT_EXAMPLE")
        assert isinstance(model.value, float)


class TestBooleanField(object):
    def test_should_non_int_raise_error(self, set_base_env):
        model = orm.BooleanField("STRING_EXAMPLE")
        with pytest.raises(orm.ConvertError):
            model.value

    def test_should_return_int(self, set_base_env):
        model = orm.BooleanField("BOOLEAN_EXAMPLE")
        assert isinstance(model.value, bool)


class TestListField(object):
    def test_should_raise_type_conv_error(self, set_base_env):
        model = orm.ListField("LIST_EXAMPLE_SINGLE", type_factory=int)
        with pytest.raises(orm.ConvertError):
            model.value


        def factory(v):
            raise ValueError

        model = orm.ListField("LIST_EXAMPLE_MULTIPLE", type_factory=factory)
        with pytest.raises(orm.ConvertError):
            model.value

    def test_should_return_int(self, set_base_env):
        model = orm.ListField("LIST_EXAMPLE_SINGLE")
        assert isinstance(model.value, list)

        model = orm.ListField("LIST_EXAMPLE_MULTIPLE", type_factory=int)
        assert isinstance(model.value, list)
        assert isinstance(model.value[0], int)


class TestEnvModel(object):

    def test_should_env_base_get_fields_correctly(self):

        class Model(orm.EnvModel):
            example = orm.StringField(
                "STRING_EXAMPLE",
            )

        settings = Model()

        assert settings._fields == ["example"]

    @pytest.mark.parametrize(
        "required, is_valid",
        (
            (True, False),
            (False, True),
        )
    )
    def test_should_not_valid_if_value_not_given(self, required, is_valid):
        class Model(orm.EnvModel):
            example = orm.StringField(
                "STRING_EXAMPLE",
                required=required,
            )

        settings = Model()

        assert settings.is_valid() is is_valid

    def test_should_type_error_cause_invalid_of_model(self, set_base_env):

        class Model(orm.EnvModel):
            example = orm.IntField(
                "STRING_EXAMPLE",
            )
        settings = Model()

        assert settings.is_valid() is False

    def test_should_output_doc(self):
        class Model(orm.EnvModel):
            example = orm.StringField(
                "STRING_EXAMPLE",
                required=True,
            )
            example1 = orm.StringField(
                "STRING_EXAMPLE_1",
                required=True,
                default='hi'
            )

        settings = Model()

        doc = "STRING_EXAMPLE=\n" + "STRING_EXAMPLE_1=hi"
        
        assert settings.doc == doc
