import time

from e2e import DockerTest
from guet.commands.init_required_decorator import INIT_REQUIRED_ERROR_MESSAGE


class TestGuetSet(DockerTest):
    def test_set_gracefully_displays_error_message_when_setting_committer_with_unknown_initials(self):
        self.guet_init()
        self.git_init()
        self.guet_set(['ui'])

        self.execute()

        self.assert_text_in_logs(1, "No committer exists with initials 'ui'")

    def test_adds_committer_initials_and_current_millis_to_committersset_file(self):
        start_time = int(round(time.time() * 1000))
        self.guet_init()
        self.git_init()
        self.guet_add('initials1', 'name1', 'email1')
        self.guet_add('initials2', 'name2', 'email2')
        self.guet_set(['initials1', 'initials2'])
        self.save_file_content('.guet/committersset')
        self.save_file_content('.guet/committers')

        self.execute()

        committers_set = self.get_file_text('.guet/committersset')

        set_text = committers_set[0]
        set_text_split = set_text.split(',')
        self.assertEqual('initials1', set_text_split[0])
        self.assertEqual('initials2', set_text_split[1])
        self.assertTrue(start_time + 10000 > int(set_text_split[2]) > start_time)

    def test_set_committer_required_init_to_have_ran_before_usage(self):
        self.guet_set(['initials1'])
        self.execute()
        self.assert_text_in_logs(0, INIT_REQUIRED_ERROR_MESSAGE)

    def test_set_committers_displays_help_message_when_no_initials_given(self):
        self.guet_init()
        self.git_init()
        self.guet_set([])
        self.execute()
        self.assert_text_in_logs(1, 'usage: guet set <initials> [<initials> ...]')

    def test_errors_if_guet_set_ran_in_folder_with_no_git(self):
        self.guet_init()
        self.guet_add('initials1', 'name1', 'email1')
        self.guet_add('initials2', 'name2', 'email2')
        self.guet_set(['initials1', 'initials2'])

        self.execute()

        self.assert_text_in_logs(0, 'Git not initialized in this directory.')
