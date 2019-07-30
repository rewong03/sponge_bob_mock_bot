import praw
import random

reddit = praw.Reddit('bot')
check_comments_path = 'checked_comments.txt'
list_of_users_to_mock = [""]


def check_comments_tag_list(list_of_comment_tag):
    """Takes a list of comment tags and removes tags whose associated comments have been replied to.

    list_of_comment_tag (list(str)): List of comment tags.

    Return:
    list_of_comment_tag (list(str)): List of comment tags with replied comment tags removed.
    """
    with open(check_comments_path, 'r') as check_comments_file:
        check_comments_list = [line.rstrip() for line in check_comments_file.readlines()]
        for comment_tag in list_of_comment_tag:
            if comment_tag in check_comments_list:
                list_of_comment_tag.remove(comment_tag)
        return list_of_comment_tag


def mock_comment(comment):
    """Takes a comment and randomly uppers and lowers letters (e.g. example -> eXaMPle).

    Parameter:
    comment (str): Comment to be mocked.

    Return:
    (str): Mocked comment.
    """
    comment_char = list(comment.lower())
    upper_or_lower_list = random.choices(['upper', 'lower'], k=len(comment_char))

    for idx, char in enumerate(comment_char):
        try:
            if upper_or_lower_list[idx] == 'upper':
                comment_char[idx] = comment_char[idx].upper()
            else:
                comment_char[idx] = comment_char[idx].lower()
        except Exception as e:
            print(e)

    return ''.join(comment_char)


def add_mocked_comment_tag(list_of_comment_tag):
    """Adds comment tag to list of checked comment tags.

    Parameter:
    list_of_comment_tag (list(str)): List of tags to add to checked comment tags file.
    """
    with open(check_comments_path, 'a') as check_comments_file:
        for comment_tag in list_of_comment_tag:
            check_comments_file.write(comment_tag + '\n')


def mock_users_comments(username):
    """Retrieves comments from user_name and replies with a mocked version of their comment.

    username (str): Username of user to mock.
    """
    user = reddit.redditor(username)
    list_of_comment_tags = []

    for comment in user.comments.new():
        list_of_comment_tags.append(comment.id)

    list_of_comment_tags = check_comments_tag_list(list_of_comment_tags)

    for comment in list_of_comment_tags:
        comment = reddit.comment(id=comment)
        comment.reply(mock_comment(comment.body))

    add_mocked_comment_tag(list_of_comment_tags)


def mock_multiple_users(list_of_users):
    """Mocks the comment of multiple users.

    Parameter:
    list_of_users (list(str)): List of users to mock.
    """
    for user in list_of_users:
        mock_users_comments(user)

mock_multiple_users(list_of_users_to_mock)








