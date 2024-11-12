from django.shortcuts import render
import random
import time

#  List of my fav quotes
quotes = [
    "The future rewards those who press on. I don't have time to feel sorry for myself. I don't have time to complain. I'm going to press on.",
    "Money is not the only answer, but it makes a difference",
    "In the end, we will remember not the words of our enemies, but the silence of our friends.",
    "No matter how much you've done or how successful you've been, there's always more to do, always more to learn and always more to achieve.",
    "Why can't I just eat my waffles?",
]

# List of image URLs
images = [
    "https://assets.editorial.aetnd.com/uploads/2016/11/white-house-qa-president-obamas-foreign-policy-legacys-featured-photo.jpg?width=828&quality=75&auto=webp",
    "https://www.history.com/the-obama-years/imgs/obamacare-obama-qa.jpg",
    "https://www.history.com/the-obama-years/imgs/obamacare-congress-speech-1.jpg",
    "https://www.history.com/the-obama-years/imgs/obamacare-obama-phone-call.jpg",
    "https://www.history.com/the-obama-years/imgs/obamacare-obama-biden-roosevelt-room.jpg",
]


def quote(request):
    """
    A view function to display one random quote and image
    This function view handles requests to the main page / and /quote
    """

    # Randomly select a quote and an image
    selected_quote = random.choice(quotes)
    selected_image = random.choice(images)

    # Pass the selected quote and image as context data to the template
    context = {
        "quote": selected_quote,
        "image": selected_image,
        "current_time": time.ctime(),
    }

    return render(request, "quotes/quote.html", context)


def show_all(request):
    """
    A function view to display all quotes and images
    This function view responds to requests to /show_all
    """
    # Pass the list of quotes and images as context to template
    context = {
        "quotes": quotes,
        "images": images,
        "current_time": time.ctime(),
    }

    return render(request, "quotes/show_all.html", context)


def about(request):
    """
    View to display information about the famous person and the app creator.
    This view handles requests to /about.
    """
    # Pass a brief biography of the famous person as context data.
    context = {
        "current_time": time.ctime(),
        "bio": "Barack Hussein Obama II (born August 4, 1961) is an American politician who served as the 44th president of the United States from 2009 to 2017.",
    }
    return render(request, "quotes/about.html", context)
