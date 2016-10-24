import gitlab
import configargparse
import re
from trello import TrelloClient
from trello.card import Card


def search_for_card_numbers(message):
    return re.findall('#(\d+)', message)


def create_link_message(commit):
    return "{} committed {}:\n{}".format(commit.author_name, commit.short_id, commit.message)


def create_gitlab_commit_url(project, commit):
    return "{}/commit/{}".format(project.web_url, commit.id)


class IntegrationEngine:

    def __init__(self, gitlab_client, trello_client):
        self.gitlab = gitlab_client
        self.trello_client = trello_client

    def commit_link_to_trello_cards(self, opts):
        commit = self.gitlab.project_commits.get(opts.gitlab_commit_id, project_id=opts.gitlab_project_id)
        project = self.gitlab.projects.get(opts.gitlab_project_id)

        for card_number in search_for_card_numbers(commit.message):
            card = self.get_card_by_board_and_number(opts.trello_board_id, card_number)
            self.attach_link_to_card(card, create_gitlab_commit_url(project, commit), create_link_message(commit))

    def attach_link_to_card(self, card, url, message):
        card.attach(name=message, url=url)

    def get_card_by_board_and_number(self, board_id, card_number):
        board = self.trello_client.get_board(board_id)
        json_obj = board.client.fetch_json(
            '/boards/' + board.id + '/cards/' + card_number,
        )
        return Card.from_json(board, json_obj)


class Options:

    def __init__(self):
        self.trello_token = None
        self.trello_api_key = None
        self.trello_board_id = None
        self.gitlab_token = None
        self.gitlab_commit_id = None
        self.gitlab_project_id = None

    def make_gitlab(self):
        return gitlab.Gitlab('https://gitlab.com', self.gitlab_token)

    def make_trello(self):
        return TrelloClient(
            api_key=self.trello_api_key,
            # api_secret=self.trello_secret,
            token=self.trello_token,
            # token_secret='your-oauth-token-secret'
        )


if __name__ == "__main__":
    parser = configargparse.ArgParser(description='Add a comment to the trello card specified in the commit message.')
    parser.add('--trello-api-key', env_var='TRELLO_API_KEY', required=True)
    parser.add('--trello-token', env_var='TRELLO_TOKEN', required=True, help='a valid aythorization token for trello')
    parser.add('--trello-board-id', env_var='TRELLO_BOARD_ID', required=True, help='a trello board id')
    parser.add('--gitlab-token', env_var='GITLAB_TOKEN', required=True)
    parser.add('--gitlab-commit-id', env_var='CI_BUILD_REF', required=True)
    parser.add('--gitlab-project-id', env_var='CI_PROJECT_ID', required=True)

    options = Options()
    parser.parse_args(namespace=options)

    IntegrationEngine(options.make_gitlab(), options.make_trello()).commit_link_to_trello_cards(options)

