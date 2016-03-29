import stripe
from identity import app

IN_GOOD_STANDING = "In Good Standing"
DELINQUENT = "Delinquent"

# Delinquent email template
D_EMAIL_TEMPLATE = """

<!DOCTYPE html>
<html>

<body>
<img src="https://synshop.org/sites/default/files/logo290.png">
<h2>Oops, it looks like your membership payments are failing.</h2>

<p>We'll still let you in the door, but please correct this as soon as possible.</p>

<p>You can modify / adjust your payment type by going here: <a href="#">https://synshop.org/user/%s/</a></p>

<p>Also, if you have any questions, please reply back to this email and we will do our best to help you.</p>

</body>
</html>

"""

def get_refresh_stripe_cache(t=None):

    stripe.api_version = '2013-02-13'
    stripe.api_key = app.config['STRIPE_TOKEN']
    member_array = []

    members = stripe.Customer.all(created={'gte':t})

    for member in members['data']:

        if (member.subscription):
            plan = member.subscription.plan.name
        else:
            plan = "No Subscription Plan"

        member_array.append({"stripe_email":member.email,"stripe_id":member.id,"member_sub_plan":plan,"description":member.description,"created":member.created})

    return member_array

def get_full_stripe_cache():

    stripe.api_version = '2013-02-13'
    stripe.api_key = app.config['STRIPE_TOKEN']

    m = 0
    c = 50

    total_customer_count = stripe.Customer.all()['count']

    member_array = []

    while m <= total_customer_count:
        members = stripe.Customer.all(offset=m,count=c)
        for member in members['data']:

            if (member.subscription):
                plan = member.subscription.plan.name
            else:
                plan = "No Subscription Plan"

            member_array.append({"stripe_email":member.email,"stripe_id":member.id,"member_sub_plan":plan,"description":member.description,"created":member.created})

        m = m + c

    return member_array

def get_payment_status(member_id=None):

    stripe.api_version = '2013-02-13'
    stripe.api_key = app.config['STRIPE_TOKEN']

    count = stripe.Customer.retrieve(member_id).subscriptions.all()['count']

    if (count != 0):
        return IN_GOOD_STANDING
    else:
        return DELINQUENT
