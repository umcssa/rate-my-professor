#!/usr/bin/env python3
"""
Test /u/<user_url_slug/ URLs.

WARNING: THIS TEST IS PUBLISHED TO STUDENTS

EECS 485 Project 2

Andrew DeOrio <awdeorio@umich.edu>
"""
import unittest
import sh
import insta485

class TestLoginLogout(unittest.TestCase):
    """Unit tests for /u/<user_url_slug>/ URLs."""

    def setUp(self):
        """Reset database, start app test client, and log in awdeorio.

        This function runs once before each member function unit test.
        """
        # Reset the database and start a test client.  Disable error catching
        # during request handling so that you get better error reports when
        # performing test requests against the application.
        try:
            insta485db = sh.Command("./bin/insta485db")
            insta485db("reset")
        except sh.ErrorReturnCode as error:
            self.assertTrue(False, ("Failed to run insta485db, "
                                    "output: "
                            "{}").format((error).decode('ascii')))
        insta485.app.config["TESTING"] = True
        self.app = insta485.app.test_client()

    def tearDown(self):
        """Reset the database.

        This function runs once after each member function unit test.
        """
        insta485db = sh.Command("./bin/insta485db")
        insta485db("reset")

    def test_index_redirect(self):
        """GET / redirects to /accounts/login/ when user is not logged in.

        Functions that start with "test" are automatically run by the unittest
        framwork.  The framework also takes care of running setUp() before each
        member function test begins and running tearDown() after each ends.
        """
        response = self.app.get("/")
        self.assertEqual(response.status_code, 302,
                         "/ did not redirect to login when user is not logged in")
        self.assertTrue(
            response.location.endswith("/accounts/login/"),
            "Redirect location did not end with /accounts/login/"
        )

    def test_login_page_content(self):
        """Verify links and form on /accounts/login/ page."""
        response = self.app.get("/accounts/login/")
        self.assertEqual(response.status_code, 200,
                         "Could not access /accounts/login/ route")
        self.assertIn(b"/accounts/create/", response.data,
                      "Couldn't find link to /accounts/create/")

    def test_login(self):
        """Login awdeorio."""
        response = self.app.post(
            "/accounts/login/",
            data={"username": "awdeorio", "password": "password"},
        )
        self.assertEqual(response.status_code, 302,
                         "Unable to login for an existing user")
        self.assertTrue(
            response.location.endswith("/"),
            "Redirect location did not end with /"
        )

    def test_logout(self):
        """Logout."""
        response = self.app.get("/accounts/logout/")
        self.assertEqual(response.status_code, 302,
                         "Unable to logout")
        self.assertTrue(
            response.location.endswith("/accounts/login/"),
            "Redirect location did not end with /accounts/login/"
        )
        # Now that we're logged out, index should redirect to login
        self.test_index_redirect()


if __name__ == "__main__":
    unittest.main(verbosity=2)
