====
CDMC - Cinco De Mayo Calendar tools
====

See the chat logs. ( at https://tilde.town/~minerobber/cdmc.txt )

Includes 2 scripts:
* cdmdate - the date in the CDM Calendar
* cdmcdateconv - A date converter to convert "plebian" normal dates into the "obviously superior" CDM format.

The module, "cdmc", includes methods:
* today() - get today in the CDM calendar
* specific_day(y,m,d) - get day y-m-d in the CDM Calendar

As well as the class Date, which has a constructor that takes a datetime.date object (defaults to datetime.date.today()) and a datetime.date object respresenting the Cinco de Mayo you want to use as a reference point, (defaults to the Cinco de Mayo that is coming up from the datetime.date.today() date) and gives you a CDM date object.


