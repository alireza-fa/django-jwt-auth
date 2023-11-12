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

Feel free to explore and contribute to this project. Any feedback and suggestions are welcome.

<h3>Documentation:</h3>
...

</div>
