import unittest
from unittest.mock import Mock, patch, call

from guet.commands.start.factory import StartCommandFactory
from guet.git.create_hook import HookMode, Hooks
from guet.settings.settings import Settings


class TestStartCommandFactoryMethod(unittest.TestCase):
    @patch('guet.commands.start.factory.PrintCommandStrategy')
    @patch('guet.commands.start.factory.StrategyCommand')
    @patch('guet.commands.start.factory.git_present_in_cwd', return_value=False)
    def test_returns_print_strategy_with_error_message_if_no_git_present(self, _, mock_strategy_command,
                                                                         mock_print_strategy):
        command = StartCommandFactory().build(['start'], Settings())
        mock_print_strategy.assert_called_with('Git not initialized in this directory.')
        mock_strategy_command.assert_called_with(mock_print_strategy.return_value)
        self.assertEqual(command, mock_strategy_command.return_value)

    @patch('guet.commands.start.factory.any_hooks_present', return_value=True)
    @patch('guet.commands.start.factory.git_hook_path_from_cwd', return_value='/path')
    @patch('guet.commands.start.factory.git_present_in_cwd', return_value=True)
    @patch('guet.commands.start.factory.PromptUserForHookTypeStrategy')
    @patch('guet.commands.start.factory.StrategyCommand')
    def test_returns_prompt_strategy_if_hooks_present(self, mock_command, mock_prompt_strategy, _1, _2, _3):
        command = StartCommandFactory().build(['start'], Settings())
        mock_prompt_strategy.assert_called_once_with('/path')
        mock_command.assert_called_once_with(mock_prompt_strategy.return_value)
        self.assertEqual(command, mock_command.return_value)

    @patch('guet.commands.start.factory.any_hooks_present', return_value=False)
    @patch('guet.commands.start.factory.git_hook_path_from_cwd', return_value='/path')
    @patch('guet.commands.start.factory.git_present_in_cwd', return_value=True)
    @patch('guet.commands.start.factory.CreateHookStrategy')
    @patch('guet.commands.start.factory.StrategyCommand')
    def test_returns_create_strategy_if_no_hooks_present(self, mock_command, mock_create_strategy, _1, _2, _3):
        command = StartCommandFactory().build(['start'], Settings())
        mock_create_strategy.assert_called_once_with('/path')
        mock_command.assert_called_once_with(mock_create_strategy.return_value)
        self.assertEqual(command, mock_command.return_value)

    @patch('guet.commands.start.factory.git_hook_path_from_cwd', return_value='/path')
    @patch('guet.commands.start.factory.git_present_in_cwd', return_value=True)
    @patch('guet.commands.start.factory.CreateAlongsideHookStrategy')
    @patch('guet.commands.start.factory.StrategyCommand')
    def test_returns_command_with_create_alongside_strategy_if_given_dash_a(self, mock_command,
                                                                            mock_alongside_strategy, _1,
                                                                            _2):
        command = StartCommandFactory().build(['start', '-a'], Settings())
        mock_alongside_strategy.assert_called_once_with('/path')
        mock_command.assert_called_once_with(mock_alongside_strategy.return_value)
        self.assertEqual(command, mock_command.return_value)

    @patch('guet.commands.start.factory.git_hook_path_from_cwd', return_value='/path')
    @patch('guet.commands.start.factory.git_present_in_cwd', return_value=True)
    @patch('guet.commands.start.factory.CreateAlongsideHookStrategy')
    @patch('guet.commands.start.factory.StrategyCommand')
    def test_returns_command_with_create_alongside_strategy_if_given_dash_dash_alongside(self, mock_command,
                                                                                         mock_alongside_strategy, _1,
                                                                                         _2):
        command = StartCommandFactory().build(['start', '--alongside'], Settings())
        mock_alongside_strategy.assert_called_once_with('/path')
        mock_command.assert_called_once_with(mock_alongside_strategy.return_value)
        self.assertEqual(command, mock_command.return_value)

    def test_get_short_help_message(self):
        self.assertEqual('Start guet usage in the repository at current directory',
                         StartCommandFactory().short_help_message())