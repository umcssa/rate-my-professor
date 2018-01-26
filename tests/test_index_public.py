#!/usr/bin/env python3
"""
Check index page at / URL.

EECS 485 Project 2

Andrew DeOrio <awdeorio@umich.edu>
"""
import unittest
import os
import insta485
import sh
import tests.util

class TestIndexPublic(unittest.TestCase):
    """Unit tests for one handcoded /index.html."""
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

    def test_comments(self):
        """Verify expected comments are present in / URL."""
        # pylint: disable=redundant-unittest-assert
        response = self.app.post(
            "/accounts/login/",
            data={"username": "awdeorio", "password": "password"},
        )
        self.assertEqual(response.status_code, 302,
                         "Unable to login for an existing user")
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200,
                      "Unable to access / route")
        soup_dict = tests.util.get_soup_dict(response.data)
        text = soup_dict["text"]
        in_cont = ["awdeorio #chickensofinstagram", "jflinn I <3 chickens",
                   "michjc Cute overload!", "awdeorio Sick #crossword",
                   "jflinn Walking the plank #chickensofinstagram",
                   "awdeorio This was after trying to teach them to " +
                   "do a #crossword"]
        out_cont = []
        check = tests.util.check_for_content(in_cont, out_cont, text)
        self.assertTrue(check, "Issue encountered with the expected text.")


if __name__ == "__main__":
    unittest.main(verbosity=2)
