import re
import jsonschema


class SchemaValidator():
    """
    Validates pubsub messages against specified schema
    """

    def validate_message(self, message):
        try:
            message.get('schema', None)
        except ValueError:
            raise ValueError('Message must contain a schema!')
        except AttributeError:
            raise AttributeError('Message must be json')
        schema_uri = message['schema']
        matches = re.findall(r'(.+)://(.+/)?events/(.+)/(.+)/(.+)\.json', schema_uri)[0]
        if matches:
            schema = jsonschema.RefResolver('', '').resolve_remote(schema_uri)
            jsonschema.validate(message, schema)
        else:
            raise ValueError('Incorrect schema uri')


class TestValidator:
    """
    Validates that message is not None
    """

    def validate_message(self, message):
        return True if (message != '') else False
