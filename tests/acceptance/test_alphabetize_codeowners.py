from texthooks.alphabetize_codeowners import main as alphabetize_codeowners_main


def test_alphabetize_codeowners_no_changes(runner):
    result = runner(alphabetize_codeowners_main, "foo")
    assert result.exit_code == 0
    assert result.file_data == "foo"

    result = runner(alphabetize_codeowners_main, "/foo/bar.txt @alice @bob")
    assert result.exit_code == 0
    assert result.file_data == "/foo/bar.txt @alice @bob"


def test_alphabetize_codeowners_normalizes_spaces(runner):
    result = runner(alphabetize_codeowners_main, " /foo/bar.txt @alice\t@bob ")
    assert result.exit_code == 1
    assert result.file_data == "/foo/bar.txt @alice @bob"


def test_alphabetize_codeowners_sorts(runner):
    result = runner(alphabetize_codeowners_main, "/foo/bar.txt @Bob @alice @charlie")
    assert result.exit_code == 1
    assert result.file_data == "/foo/bar.txt @alice @Bob @charlie"


def test_alphabetize_codeowners_sorts_other(runner):
    result = runner(
        alphabetize_codeowners_main,
        "/foo/bar.txt @Andy @adam @Bob @alice @charlie @groß @grost @grose",
    )
    assert result.exit_code == 1
    assert (
        result.file_data
        == "/foo/bar.txt @adam @alice @Andy @Bob @charlie @grose @groß @grost"
    )


def test_alphabetize_codeowners_ignores_non_semantic_lines(runner):
    result = runner(
        alphabetize_codeowners_main,
        """
# comment 1: some comment

# comment 2: some non-alphabetized strings
# d c b a
/foo/bar.txt @alice @charlie""",
    )
    assert result.exit_code == 0
