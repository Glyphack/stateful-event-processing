from datetime import datetime
from mock_data import publisher

users_data = [
    {
        "email": "shayegan@mail.com",
        "username": "glyphack",
        "registered_at": datetime.now().timestamp(),
        "type": "person",
    },
    {
        "email": "farbod@mail.com",
        "username": "farbod",
        "registered_at": datetime.now().timestamp(),
        "type": "person",
    },
]

users_avro_schema = """
{
  "namespace": "github",
   "name": "user",
   "type": "record",
   "fields" : [
     {
       "name" : "email",
       "type" : "string"
     },
    {
       "name" : "username",
       "type" : "string"
     },
     {
       "name" : "registered_at",
       "type" : "int",
       "logical_type": "date"
     },
     {
       "name" : "type",
       "type" : {
          "name": "EnumType",
          "type": "enum",
          "symbols" : ["org","person"]
        }
     }
   ]
}
"""

publisher.bulk_publish(users_avro_schema, users_data)
