from django.db.models import ForeignKey


def get_required_fields(model):
    fields = model._meta.get_fields()
    required_fields = []

    # Required means `blank` is False
    for f in fields:
        # Note - if the field doesn't have a `blank` attribute it is probably
        # a ManyToOne relation (reverse foreign key), which you probably want to ignore.
        if hasattr(f, 'blank') and f.blank == False and not isinstance(model._meta.get_field(f.name), ForeignKey):
            required_fields.append(f.name)
    return required_fields


def get_optional_fields(model):
    fields = model._meta.get_fields()
    optional_field = []

    # Required means `blank` is False
    for f in fields:
        # Note - if the field doesn't have a `blank` attribute it is probably
        # a ManyToOne relation (reverse foreign key), which you probably want to ignore.
        if not (hasattr(f, 'blank') and f.blank == False):
            optional_field.append(f.name)
    return optional_field
