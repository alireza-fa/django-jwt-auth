# Django JWT Auth

<div>

<h3>Introduction:</h3>

This is a project for user authentication using the JWT system, with a primary focus on efficiency, reusability in different
projects, and high security.

The django_simple_jwt package has been used for JWT implementation.

<h3>UserLogin model</h3>
In this project, we have a model called UserLogin which stores user login information such as refresh_token,
device_name, and ip_address. With this setup, we can effectively manage user logins and also implement restrictions
on logged-in devices.

<h3>Token Encryption:</h3>

Tokens are sent to the client in an encrypted form, ensuring that no one can see the contents of the token's payload.
This provides excellent security. Additionally, by encrypting the tokens, we can include any necessary information
that needs to be sent in each request for the user in the payload. However, it is not recommended to include highly
sensitive information in the payload.

User login and account verification are done by default using OTP codes. However, you can easily modify it according
to your preference, as explained in the documentation provided below.

Having a good caching mechanism, such as Redis or Memcached, is also recommended in real-world projects.

Please refer to the documentation below for further details on how to use and customize this project.

<h3>How to use this project</h3>
Since the authentication requirements vary for different systems, it is not possible to create a project that can meet
our needs without any modifications.

One system may use email and login code for authentication, while another system may require a username and password,
and so on. Therefore, it is not feasible to handle all these scenarios in a single project.

However, in this project, I have simplified the process as much as possible. You only need to customize the services.py
module and define its corresponding views and URLs.
Operations such as token encryption, token retrieval, and account logout do not require any modifications.

To understand how to write the services.py module for your own project, refer to the views.py section of the user_auth
app and read the documentation for each view. In general, you need to make any desired changes while ensuring that the
output of the functions is compatible with the views. If you require more extensive modifications, you can also
customize the views.

Feel free to explore and contribute to this project. Any feedback and suggestions are welcome.
</div>
