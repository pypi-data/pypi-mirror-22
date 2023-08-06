==================
Emtex Common Utils
==================

This contains utility like permissions, audit log etc.

Detailed documentation is in the "docs" directory.

How to install
--------------

1. Using pip::

    pip install emtex_common_utils==0.3
        or
    Add emtex_common_utils==0.3 in your requirements.txt file and then run:
    pip install -r requirements.txt


Quick start
-----------

1. Add "emtex_common_utils" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'emtex_common_utils',
    ]


Things available
----------------

1. Database Migrations::

    python manage.py emtex_migrate --for_date="YYYY-MM-DD"

2. Logging::

    from emtex_common_utils.models import BaseModel, BaseLogModel
    from emtex_common_utils.mixins import BaseModelMixin

    ...


    class MyModelLog(BaseLogModel):
        """ Model to log changes for model MyModel """
        pass


    class MyModel(BaseModel, BaseModelMixin):
        """ Model which changes needs to be tracked. """

        class Meta:
            log_fields = (
                my_field1, my_field2,
                ...
            )
            log_model_name = MyModelLog

