import gitlab
import configargparse
import re


def main(options):
    gl = gitlab.Gitlab('https://gitlab.com', options.gitlab_token)
    client = TrelloClient(
            api_key='your-key',
            api_secret='your-secret',
            token='your-oauth-token-key',
            token_secret='your-oauth-token-secret'
    )

    commit = gl.project_commits.get(options.gitlab_commit_id, project_id=options.gitlab_project_id)
    commit.message
    commit.url
    commit.author_name

    for card_number in search_for_card_numbers(commit.message):
        # TODO
        card_id = get_card_id_by_board_and_number(options.trello_board_id, card_number)
        attach_link_to_card(card_id, commit.url, create_link_message(commit.author_name, commit.message))


def search_for_card_numbers(message):
    return re.findall('#(\d+)', message)


class ApiBroker

class Options:
    def __init__(self):
        self.trello_token = None
        self.trello_board_id = None
        self.gitlab_token = None
        self.gitlab_commit_id = None
        self.gitlab_project_id = None


if __name__ == "__main__":
    parser = configargparse.ArgParser(description='Add a comment to the trello card specified in the commit message.')
    parser.add('--trello-token', env_var='TRELLO_TOKEN', required=True, help='a valid aythorization token for trello')
    parser.add('--trello-board-id', env_var='TRELLO_BOARD_ID', required=True, help='a trello board id')
    parser.add('--gitlab-token', env_var='GITLAB_TOKEN', required=True)
    parser.add('--gitlab-commit-id', env_var='CI_BUILD_REF', required=True)
    parser.add('--gitlab-project-id', env_var='CI_PROJECT_ID', required=True)

    options = Options()
    parser.parse_args(namespace=options)

    main(options)

