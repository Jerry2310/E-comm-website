# E-comm-website
Django based E-commerce website using Bootstrap, Javascript, Python, and Django framework with some more extra technology in core functionalities.

## Lessons Learned

Ecommerce is the most economical way to grow your retail business. It doesn’t require high levels of initial capital and it’s very cost-effective. Most of the investment is repaid by early sales profits. 24*7/365 availability of goods and unlimited customer reach generate more sale. The most convenient aspect of ecommerce is that the customer can purchase directly from you after searching for an item online, without leaving home or interacting with a salesperson. Customer advocacy and increased brand awareness help reduce marketing and advertising costs. 

## Tech Stack

**Client:** React, HTML, CSS, Bootstrap

**Server:** Javascript, Django, python


## Deployment

To deploy this project run

```bash
  npm manage.py runserver
```
## Run Locally

Clone the project

```bash
  git clone "link of project"
```

Go to the project directory

```bash
  cd ecommerce
```

Install dependencies

```bash
  npm install *
```

Start the server

```bash
  npm manage.py runstrver
```

# models define
- register(optional)
- login(optional)
- logout(optional)
- coustomer
- store 
- order
- order item
- shipping address

# Extras
Here the login and logout pages are also provided which are commented out in views.py , url.py and main.html file which also can be use directly you just you have to give the a code in href={% url 'store' %} in logot button in main file.
