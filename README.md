# Team member

Chaisiri Onlim 6510615062

Tanapat Sa-nguantud 6510615120

# CN331-assignment2

## For users

We've built a quota registration system using Django framework.

The web-application contains 3 html page: sign-in, sign-up and dashboard.

The web-application has a default url set to the sign in page.

Users can redirect to the signup page and enter information to create an account.

After signing up the website redirects user to sign in again.

After user signs in, the website will redirect user to the dashboard page.

The dashboard is inaccessible without signing in.

The dashboard page contains three main elements:
- your registered course table at the top (maximum of 7 courses)
    * click button "delete" to withdraw a registered course 
- search bar
    * using course ID to search
- table contains all the courses
    * with filtering button to see the course open for registration (Status = Open)

A prevention system in case more than one user try to enroll into a same course with only one seat left.

A sign-out button at the top right corner.

The dark mode/light mode switch icon is on the navigation bar.

## For admin

By signing in via the sign-in page the website will redirect to the Django administration page.

You can edit information about Students, Registrations, and Courses.

## Demonstration video

[Watch the video](https://youtu.be/Re_aVNl9H20)












