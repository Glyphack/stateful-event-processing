conf = {
    'topic_name': 'user',
    'table_name': 'users',
    'table_schema': ["id SERIAL PRIMARY KEY"],
    'event_field_to_table_mapping': {
        'email': 'email',
        'username': 'username',
        'registered_at': 'registered_at'
    }
}