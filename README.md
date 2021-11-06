# bilonga
Useless reverse proxy, middleware or "that shit that stays in the middle" (whaterver you wanna call it, we call it Bilonga)

## Usage
```python
import bilonga

my_app = bilonga.Bilonga()

@my_app.connection_handler(81,8081)
def my_handler(data):
    if data == 'hello\n':
        return data + "this is a hello", True # allow data flow
    return data + "this is NOT a hello", False # this gets filtered

my_app.run()
```

**Obs:** handlers should always return `new_data` and a boolean `allow_data_flow` that specifies whether to
pass the data through or not.
