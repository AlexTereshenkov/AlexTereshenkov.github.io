title: What I think a great tech support should look like
date: 2020-08-05
modified: 2020-08-11
author: Alexey Tereshenkov
tags: tech-support
slug: my-version-of-a-great-tech-support
category: tech-support

Being a software engineer implies that you may be interacting with customers particularly if you 
are working in a small company.
If you wearing multiple hats or if you are in professional services or tech support, 
you will likely be contacted by your customers about issues they may experience using your 
product -- a web site, a desktop or a mobile app, or some hardware equipment.

Whatever it is, I believe it's best to have a clear plan of actions outlined which you can 
follow when addressing a customer's issue. No matter how fine-grained your protocol of 
communication with the customer already is, you can always incorporate some of the ideas 
I have about how I'd like to work with a customer that needs help.

I do understand that it may be difficult or unrealistic to follow the steps below exactly,
but this is my vision of a great support.

### Customer gets in touch

Customer reaches out to you because some functionality on the web site of a business
system your team built doesn't work as they expect. 

### Pace yourself

Do not attempt to provide any solution or ask any questions just yet.
If your guess will be accurate -- you ask to enable JavaScript in a web browser or to log
out and log back in -- the customer is less likely to share any details with you because 
they can now continue working.

You, on the other hand, are missing a chance to document the incident to see if it would be
possible to prevent it from happening again and to share it with your team members. 
What was the version of the web browser where the JavaScript is not enabled by default?
Did they really have to log out and log back in or a simple refresh of a web page would be
enough (you may tweak server-side caching settings)?
You may never figure this out and even though the problem is "solved" and the customer is happy,
in the long run this was a lost.

### Show empathy

No matter what channel of communication is being used -- a phone call or an email -- the
first thing you do is to show some empathy: being an engineer, you know better than anyone 
how frustrating it can be when a computer doesn't do what you want it to do.

### Collect information

You can start collecting the information you will need to troubleshoot now; don't ask for
information you can collect yourself, but sometimes it may still be useful -- even if you can 
SSH into a server to get the version of a software installed, it would still be 
very useful to ask the customer to tell you the version they see on the web page as an older
version may indicate a web page caching issue.
You would ideally have a pre-defined template document where you can fill all the information
you may need so that you don't have think about it during a phone call.

### Share information

Once you have gathered all the information, make sure to share it with the customer.
If on the phone, read it back to them.
If it's an email conversation, either share the complete document or provide access to the
internal support system (if any) where they would be able to check that the information
they've shared with you is accurate.
This will help to avoid any misunderstandings and provide traceability as the customer
will acknowledge that the information they have provided is correct.

### Doing troubleshooting

Depending on how urgent the request is, you may or may not have time to do some manual
production inspection before telling the customer how to fix their problem.
If they are in a middle of a presentation to a board of directors, it may be best to tell them
how to fix the issue immediately.

If it is not time critical, you may want to ask for some time to log in into the production
environment to record as much as information as you possibly can.
For instance, they told you that they are still able to use the system despite not being
logged in. Instead of telling them to log off and log in hoping it will fix the problem
(did you know that [hope is not a strategy](https://landing.google.com/sre/sre-book/chapters/introduction/)?), 
you may want to log in into the server to find out what's going on with your
authentication service while the user hasn't left their web browser session (provided you
don't do any verbose logging of this type of events already).
This issue may indicate some serious problem that is worth investigating further because
it may manifest itself again at some point.

### Update on the progress

If the problem requires more time and you will likely need to spend hours if not days
working on it, it's best to let the customer know about the progress.
They would be able to find it very helpful to see that you are working on their issue and
ideally how much time you've spent (a support ticket can be "in progress" for 5 days, but
the engineer may have been working on it for just 1 hour).

### Provide a temporary solution if applicable

If it's an option, make sure to provide customer with a workaround to let them continue to 
do their business.
If they need to process some files, offer to do it manually for them if possible.
If their business operation depends on a feature from their "basic" plan 
that doesn't work and you know that an alternative feature from the "advanced" plan would work,
upgrade their account for some time while you are troubleshooting.

### Tell about proposed solution

Once you have identified the issue and have been able to solve it, tell the user what was
happening and what you have done to solve it.
Adjust the language depending on how technical things get as required but don't be afraid to offer
them a chance to learn; many customers would find it helpful to understand how the product they
use operate under the hood.
Ask them to verify that the solution you've implemented works for them (after you have done everything
you possibly could to verify this yourself first).
 
### Document your findings

After you found the resolution to a problem, make sure to document not only what has to be done to fix it,
but also what have you attempted to get done which didn't seem to help.
For instance, you thought that the problem may be due to a broken database table index and have decided
to re-build it.
That didn't help and then you think that perhaps recalculating the table statistics may help.
You do that now and, yes, the problem is gone.

However, documenting that for this problem recalculating the table statistics is necessary may be misleading
as re-building the table index may also be required.
When you or a colleague of yours will be reading the incident documentation, they will know what
have you attempted before finding the solution.
Wherever possible, any changes to any environment should be happening via code or a terminal to make
it easy to record as making changes in the GUIs are generally known to be very hard to document.

A problem that can be solved purely by customers themselves (invalidating the web browser cache or
to change some setting within the user interface of the business system itself) is a great candidate
to be added into the user documentation.

Happy supporting!
