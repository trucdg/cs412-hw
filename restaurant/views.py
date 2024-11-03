from django.shortcuts import render, redirect
import time, random
from datetime import datetime, timedelta


# Create your views here.
def main(request):
    """
    A view function handling requests to /restaurant/main
    render with template main.html
    """
    template_name = "restaurant/main.html"

    # Context data for the main page (name, location, hours, photos)
    context = {
        "current_time": time.ctime(),
        "name": "Pho 89 Brockton",
        "location": "708 Belmont St, Brockton, MA 02301",
        "hours": ["Mon-Fri: 9:00am - 10:00pm", "Sat-Sun: 10:00am - 11:00pm"],
        "photos": [
            "https://www.enterprisenews.com/gcdn/authoring/authoring-images/2024/05/18/NENT/73749325007-05182024-mv-brockton-food-21.JPG?width=1200&disable=upscale&format=pjpg&auto=webp",
            "https://s3-media0.fl.yelpcdn.com/bphoto/J75xZymFFmAeHDwMxcM8sw/o.jpg",
            "https://www.dailynews.com/wp-content/uploads/2023/01/LDN-L-DINE-PHO-0113-01-03.jpg?w=525",
        ],
    }

    return render(request, template_name, context)


# Global variables to use in the order and submit view
# Dict of regular dishes and their prices
dishes = {
    "Wonton Soup": 8,
    "Egg Rolls": 6,
    "Beef Noodle Soup with Brisket": 15,
    "Special Combination Beef Noodle Soup": 16,
}

# Extra toppings for the special combination and their prices
toppings = {
    "Extra Vegetables": 2,
    "Extra Meatballs": 3,
    "Extra Brisket": 4,
    "Tendon": 3,
}

# Dict of special dishes
specials = {"Spring Rolls": 7, "Sate Beef Udon": 16, "Grilled Chicken Vemicelli": 15}


def order(request):
    """
    Handle requests to url endpoint /restaurant/order
    Render with template order.html
    Display the order page where customers can select pho noodle soup and other Vietnamese dishes.
    Pass a random "daily special" item to the order.html template
    """
    # Randomly select a daily special
    daily_special_name = random.choice(list(specials.keys()))
    daily_special_price = specials[daily_special_name]

    # argument for the order.html template
    context = {
        "current_time": time.ctime(),
        "dishes": dishes,
        "toppings": toppings,
        "daily_special": {
            "name": daily_special_name,
            "price": daily_special_price,
        },
    }

    return render(request, "restaurant/order.html", context)


def confirmation(request):
    """
    Handle the form submission and confirmation
    Read data from the request and send it back to confirmation.html
    """

    template_name = "restaurant/confirmation.html"

    total_price = 0

    # Handle form submission
    if request.POST:
        # get selected items and toppings
        print(request.POST)

        selected_items = request.POST.getlist("items")
        selected_toppings = request.POST.getlist("extras")
        selected_daily_special = request.POST.get("daily_special")

        # Retrieve the customer's personal information
        customer_name = request.POST.get("name")
        customer_phone = request.POST.get("phone")
        customer_email = request.POST.get("email")

        # Retrieve special instructions
        special_instructions = request.POST.get("instructions", "")

        # Calculate total price based on selected dishes and extras
        for item in selected_items:
            total_price += dishes.get(item, 0)

        for topping in selected_toppings:
            total_price += toppings.get(topping, 0)

        # Add price for daily special if selected
        if selected_daily_special:
            daily_special_price = specials.get(selected_daily_special, 0)
            total_price += daily_special_price

            # Generate a random ready time (30-60 minutes from now)
        ready_time = datetime.now() + timedelta(minutes=random.randint(30, 60))

        # Context to pass to the confirmation page
        context = {
            "customer_name": customer_name,
            "customer_phone": customer_phone,
            "customer_email": customer_email,
            "selected_items": selected_items,
            "selected_toppings": selected_toppings,
            "selected_daily_special": selected_daily_special,
            "special_instructions": special_instructions,
            "total_price": total_price,
            "ready_time": ready_time.strftime("%I:%M %p"),
            "current_time": time.ctime(),
        }

        return render(request, template_name, context)

    # Handle GET request on this url
    return redirect("restaurant:order")
