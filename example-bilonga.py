import bilonga

app = bilonga.Bilonga()

@app.connection_handler(81,8081)
def my_handler(data):
    if data == 'hello\n':
        # return True, data
        return data + "this is a hello"
    return data + "this is NOT a hello"

app.run()
