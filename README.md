# how to use Tireless.

### configuring tailwindcss file
add the following in "tailwindcss.config.js"
```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.{html,j2}"],
  theme: {
    extend: {},
  },
  plugins: [],
}

```
# How to create a Tireless application basing on Flask
first import the following in your app.py

```python
from tireless import app
from bp.blueprint import bp
from tireless import run
```
define your application

```python
@app.route("/")
def Index():
    return "Hello world"
```
add the following lines of codes to ensure your app will run
```python
if __name__=="__main__":
    run(debug=True)
```

then run your application
```python
$ python app.py
````
open the link to the server