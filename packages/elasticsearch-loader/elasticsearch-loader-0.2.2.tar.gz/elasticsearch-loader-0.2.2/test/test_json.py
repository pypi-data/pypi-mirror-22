from click.testing import CliRunner
from elasticsearch_loader import cli
import mock


def invoke(*args, **kwargs):
    content = """[{"id": "MOZA", "first": "Moshe", "last": "Zada"},
                     {"id": "MICHO", "first": "Michelle", "last": "Obama"},
                     {"id": "a", "first": "b", "last": "c"},
                     {"id": "d", "first": "e", "last": "f"}]"""
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open('sample.json', 'w') as f:
            f.write(content)
        return runner.invoke(*args, **kwargs)


@mock.patch('elasticsearch_loader.single_bulk_to_es')
def test_should_iterate_over_json(bulk):
        result = invoke(cli, ['--index=index', '--type=type', 'json', 'sample.json'], catch_exceptions=False)
        assert result.exit_code == 0
        assert filter(None, bulk.call_args[0][0]) == ({'first': 'Moshe', 'id': 'MOZA', 'last': 'Zada'},
                                                      {'first': 'Michelle', 'id': 'MICHO', 'last': 'Obama'},
                                                      {'first': 'b', 'id': 'a', 'last': 'c'},
                                                      {'first': 'e', 'id': 'd', 'last': 'f'})


@mock.patch('elasticsearch_loader.single_bulk_to_es')
def test_should_iterate_over_json_bulk_size_1(bulk):
        result = invoke(cli, ['--bulk-size=1', '--index=index', '--type=type', 'json', 'sample.json'], catch_exceptions=False)
        assert result.exit_code == 0
        assert bulk.call_count == 2
        assert filter(None, bulk.call_args[0][0]) == (({'first': 'e', 'id': 'd', 'last': 'f'},))
