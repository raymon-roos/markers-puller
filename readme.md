# Guide

**Step 1:**
Open your Markers and log in.

**Step 2:**
Go to inspect element.

![Screenshot](assets/to_inspect_element.png)

**Step 3:**
Go to the network tab in the element inspector.
This is sometimes in the lint:

![Screenshot](assets/network_in_lint.png)

But can also be in a hamburger menu like this:

![Screenshot](assets/network_in_hamburger.png)

**Step 4:**
Refresh the Markers page with the network tab open.
If it went well, you would see something like this in the network tab:

![Screenshot](assets/network_after_refresh.png)

**Step 5:**
We are searching for a specific part in here and we can easily find it by sorting things on time by clicking 2 times on the time part in the network tab so there is a downwards arrow next to "time":

before:

![Screenshot](assets/before_click.png)

after:

![Screenshot](assets/after_click.png)

**Step 6:**
Click on the part that i probably at the top because it took long to load and if not, its name starts with "evaluation" and has an orange ";" in front of it:

before:

![alt text](assets/evaluation_api.png)

after:

![alt text](assets/api_after_click.png.png)