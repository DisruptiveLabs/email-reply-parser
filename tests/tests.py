import unittest
from context import email_reply_parser
from email_reply_parser import EmailReplyParser


class EmailMessageTest(unittest.TestCase):

    def test_simple_body(self):
        message = self.get_email('email_1_1')

        self.assertEquals(3, len(message.fragments))
        self.assertEquals([False, True, True],
            map(lambda x: x, [f.signature for f in message.fragments]))
        self.assertEquals([False, True, True],
            map(lambda x: x, [f.hidden for f in message.fragments]))
        self.assertTrue("folks" in message.fragments[0].content)
        self.assertTrue("riak-users" in message.fragments[2].content)

    def test_reads_bottom_message(self):
        message = self.get_email('email_1_2')

        self.assertEquals(6, len(message.fragments))
        self.assertEquals([False, True, False, True, False, False],
            map(lambda x: x, [f.quoted for f in message.fragments]))

        self.assertEquals([False, False, False, False, False, True],
            map(lambda x: x, [f.signature for f in message.fragments]))

        self.assertEquals([False, False, False, True, True, True],
            map(lambda x: x, [f.hidden for f in message.fragments]))

        self.assertTrue("Hi," in message.fragments[0].content)
        self.assertTrue("On" in message.fragments[1].content)
        self.assertTrue(">" in message.fragments[3].content)
        self.assertTrue("riak-users" in message.fragments[5].content)

    def test_reads_top_post(self):
        message = self.get_email('email_1_3')

        for f in message.fragments:
            print '=== begin frag ==='
            print f.content
            print '=== end frag ==='

        self.assertEquals(5, len(message.fragments))

    def test_multiline_reply_headers(self):
        message = self.get_email('email_1_6')

        self.assertIn('I get', message.read().text)
        self.assertRegexpMatches('^On', str(message.text))

    def test_captures_date_string(self):
        message = self.get_email('email_1_4')

        self.assertTrue('Awesome' in message.fragments[0].content)
        self.assertTrue('On' in message.fragments[1].content)
        self.assertTrue('Loader' in message.fragments[1].content)

    def test_complex_body_with_one_fragment(self):
        message = self.get_email('email_1_5')

        self.assertEquals(1, len(message.fragments))

    def test_verify_reads_signature_correct(self):
        message = self.get_email('correct_sig')
        self.assertEquals(2, len(message.fragments))

        self.assertEquals([False, False],
            map(lambda x: x, [f.quoted for f in message.fragments]))

        self.assertEquals([False, True],
            map(lambda x: x, [f.signature for f in message.fragments]))

        self.assertEquals([False, True],
            map(lambda x: x, [f.hidden for f in message.fragments]))

        self.assertTrue('--' in message.fragments[1].content)

    def test_deals_with_windows_line_endings(self):
        msg = self.get_email('email_1_7')

        self.assertRegexpMatches(msg.fragments[0].content, ':\+1:')
        self.assertRegexpMatches(msg.fragments[1].content, 'On')
        self.assertRegexpMatches(msg.fragments[1].content, 'Steps 0-2')

    def test_reply_parsed(self):
        pass

    def get_email(self, name):
        """ Return EmailMessage instance
        """
        text = open('emails/%s.txt' % name).read()
        return EmailReplyParser.read(text)


if __name__ == '__main__':
    unittest.main()
