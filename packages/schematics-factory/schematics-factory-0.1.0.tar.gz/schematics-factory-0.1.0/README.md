Schematics Factory
==================


Inspired by [Voluptuous](https://github.com/alecthomas/voluptuous).

It's sometimes inconvenient to define
named [Schematics](https://github.com/schematics/schematics)
Models, especially when those models are deeply nested.

Example:

```
class InnerModel(Model):
    inner_bool = BooleanType()


class MiddleModel(Model):
    middle_int = IntType()
    middle_nested = ModelType(InnerModel)


class OuterModel(Model):
    outer_str = StringType()
    outer_nested = ModelType(MiddleModel)


model_instance = OuterModel(input_)
model_instance.validate()
```

So, this library provides a convenient syntax for defining
deeply nested Models.

```
from schematics_factory import model

OuterModel = model({
    'outer_str': StringType(),
    'outer_nested': ModelType(model({
        'middle_int': IntType(),
        'middle_nested': ModelType(model({
            'inner_bool': BooleanType()
        }))
    }))
})

model_instance = OuterModel(input_)
model_instance.validate()
```

The model() function can also be imported as _model_factory_.

Alternative Syntax
------------------

Schema factory arguments can also be supplied as keyword
arguments rather than a dictionary.

```
Person = model(name=StringType(), age=IntType())

person = Person(dict(name='Test', age=27))

person.validate()
```

For nested Models, a concise __nested()__ convenience function
is provided to replace ModelType(model(...)) with nested(...).
The nested() function can also be imported as _nested_model_.

```
from schematics_factory import model, nested

Person = model(name=StringType(), pet=nested(name=StringType()))

person = Person(dict(name='Test', pet=dict(name='Rover')))

person.validate()
```

Nested models can also be provided as plain dictionary literals.

```
Person = model(name=StringType(), pet=dict(name=StringType()))

person = Person(dict(name='Test', pet=dict(name='Rover')))

person.validate()
```

Or equivalently...

```
Person = model({
    'name': StringType(),
    'pet': {
        'name': StringType()
    }
})

person = Person({
    'name': 'Test',
    'pet': {
        'name': 'Rover'
    }
})

person.validate()
```
