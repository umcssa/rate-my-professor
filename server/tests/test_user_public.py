#!/usr/bin/env python3
"""
Test /u/<user_url_slug/ URLs.

EECS 485 Project 2

Andrew DeOrio <awdeorio@umich.edu>
"""
import unittest
import os
import insta485
import sh
import tests.util

class TestUserPublic(unittest.TestCase):
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
        self.app_context = insta485.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """Reset the database.

        This function runs once after each member function unit test.
        """
        self.app_context.pop()
        insta485db = sh.Command("./bin/insta485db")
        insta485db("reset")

    def test_awdeorio(self):
        """Check default content at /u/awdeorio/ URL."""
        # pylint: Disable=redundant-unittest-assert
        response = self.app.post(
            "/accounts/login/",
            data={"username": "awdeorio", "password": "password"},
        )
        self.assertEqual(response.status_code, 302,
                         "Unable to login for an existing user")
        response = self.app.get("/u/awdeorio/")
        self.assertEqual(response.status_code, 200,
                      "GET /u/awdeorio/ did not return 200.") 

        soup_dict = tests.util.get_soup_dict(response.data)
        links = soup_dict["links"]
        srcs_a = soup_dict["srcs_a"]
        text = soup_dict["text"]
        buttons = soup_dict["buttons"]
        # Every page should have these
        self.assertTrue(tests.util.check_header(links),
                        "Can't find an element in the header.")
        # Links specific to /u/awdeorio/followers/
        in_cont = ["/u/awdeorio/followers/", "/u/awdeorio/following/",
                   "/p/1/", "/p/3/"]
        out_cont = ["/u/jflinn/followers/", "/u/jflinn/following/",
                    "/u/michjc/followers/",
                    "/u/michjc/following/", "/u/jag/followers/",
                    "/u/jag/following/", "/p/2/", "/p/4/"]
        check = tests.util.check_for_content(in_cont, out_cont, links)
        self.assertTrue(check, "Issue encountered with the expected links.")

        # Check for images
        in_cont = [tests.util.POST_1, tests.util.POST_3]
        out_cont = [tests.util.POST_2, tests.util.POST_4]
        check = tests.util.check_for_content(in_cont, out_cont, srcs_a)
        self.assertTrue(check, "Issue encountered with the expected images.")

        # Check for text
        in_cont = ["2 posts", "2 followers", "2 following", "Andrew DeOrio",
                    "Edit profile", "logout"]
        out_cont = ["not following", "login"]
        check = tests.util.check_for_content(in_cont, out_cont, text)
        self.assertTrue(check,
                        "Issue encountered with text or proper English.")

        self.assertEqual(2, text.count("awdeorio"),
                         "Issue encountered with the expected text.")
        self.assertEqual(1, text.count("following"),
                         "Issue encountered with the expected text.")

        #Check for buttons
        in_cont = ["file", "create_post"]
        out_cont = ["delete_post", "delete"]
        check = tests.util.check_for_content(in_cont, out_cont, buttons)
        self.assertTrue(check, 
                        "Could not find buttons on /u/awdeorio/")


if __name__ == "__main__":
    unittest.main(verbosity=2)
