## **Votely — Instant Customer Feedback Made Simple**

#### Video Demo:  https://www.youtube.com/watch?v=JZqKmqTKz8o

In a world where customer expectations move fast, businesses need feedback that is immediate, easy to collect, and simple to understand. Traditional surveys are often too long, emails go unanswered, and feedback forms are forgotten. **Votely** changes that by making feedback effortless - for both businesses and customers.

Votely is a lightweight yet powerful feedback platform that helps businesses collect real-time opinions through shareable links and interactive voting screens. Whether you want detailed feedback from customers after a visit or quick impressions from people walking past your location, Votely gives you the tools to gather responses instantly and turn them into clear insights through a live dashboard.

---

## **Create Feedback Links in Seconds**

Getting started with Votely is intentionally simple. You create an account, and go to the dasshboard, and Votely instantly generates a unique link that customers can open from any device. No app downloads, no logins, and no friction.

These links can be shared in many different ways:

- Email follow-ups after a purchase
- SMS messages
- QR codes printed at checkout or tables
- Social media posts
- Digital receipts or invoices
- Customer support conversations

Because the forms are designed for speed and clarity, customers can complete them in just a few seconds. This dramatically increases response rates and helps businesses collect honest, timely feedback while the experience is still fresh in the customer’s mind.

---

## **Two Ways to Gather Feedback**

One of Votely’s biggest strengths is flexibility. Businesses can collect feedback in two distinct ways depending on their environment and goals.

### **1. Shareable Feedback Form Links**

The first method uses a standard feedback link that opens a clean, mobile-friendly form. This option is perfect for collecting structured input after a customer interaction. Businesses can get a rating and gather short written comments to measure satisfaction.

These forms work well for:

- Service-based businesses
- Online purchases
- Appointment follow-ups
- Event attendees
- Customer support interactions

Because the experience is quick and distraction-free, customers are more likely to finish the form, giving businesses higher-quality data.

### **2. Full-Screen Tablet Voting Mode**

The second method is designed for in-person environments. Votely provides a dedicated full-screen voting link that can be opened on a tablet or kiosk. Once launched, the device displays a simple voting interface that customers can interact with while walking past.

This setup is ideal for:

- Retail stores
- Trade shows
- Conferences
- Restaurants and cafés
- Reception areas
- Pop-up events

Customers simply tap a button to rate their experience — no typing, no sign-up, no delays. The interface is intentionally visual and clear, allowing people to participate within seconds. After each vote, the screen resets automatically, making it ready for the next person.

This walk-by voting experience helps capture feedback from people who might never fill out a traditional survey but are happy to tap once on a screen. Over time, these quick interactions create a powerful stream of real-world insight.

---

## **Files**

### **1. app.py**

This is the main file with all the routes backend behind the website.

### **2. votely.db**

This is the database where all user data and votes are securely stored.

### **3. templates**

This is the folder where all the html files are stored.
In index.html theres the landing page, you see when you open the site.
To register theres the register.html and for login there's the login.html.
After you created an account you can go to the dashboard on dashboard.html. On the dashboard, you can see how many votes you got in the last day, week, year and total.
Theres also A few charts I made with chart.js of which one shows a graph with the number of votes over time and the second shows a piechart with the votes.
Under there there's a table with all votes. You can expand it and see just the table with all votes in votes.html and you can also download all the votes as a csv file.
In the dashboard are also the links for your form link and also the on-site link, which you can just copy with the click of a button and send to your customers.
If theres an error you get taken to error.html where you see a cute little hamster.
On the on-site link, there are three emojis representing good, medium and bad rating and when you click one of them you get taken to the thank you page, where you get thanked and get redirected to the main page after 5 seconds.
On the form link, theres a form with the three emojis again but also with the option to leave a comment.

---

## **Design**

I intentionaly decided to use two different design to seperate the customer view of the business view of the website.
So for all the pages like the dashboard, which the businesses should see, I've chosen a dark blue theme.
And for all the customer sites like the form, I've chosen a light, standard theme.
