from diglab_utils.test_utils import (test_directory, initialize_test_dir)
from elab_bridge.server_interface import (upload_template, upload_experiment,
                                          delete_template, delete_experiment, extended_download)

SERVER_CONFIG_YAML = (test_directory / 'testfiles_elab' / 'TestProject' / 'project.json').resolve()


def test_upload_template(initialize_test_dir):
    template_file = test_directory / 'testfiles_elab' / 'template.json'
    template, template_id = upload_template(server_config_json=SERVER_CONFIG_YAML,
                                            template_file=template_file,
                                            template_title='Testproject')

    assert 'elabftw' in template
    assert 'extra_fields' in template

    # cleanup
    delete_template(server_config_json=SERVER_CONFIG_YAML, template_id=template_id)


def test_upload_experiment(initialize_test_dir):
    template_file = test_directory / 'testfiles_elab' / 'experiment.json'

    experiment, experiment_id = upload_experiment(server_config_json=SERVER_CONFIG_YAML,
                                                  experiment_file=template_file,
                                                  experiment_title='TestExperiment')

    assert 'extra_fields' in experiment

    # cleanup
    delete_experiment(server_config_json=SERVER_CONFIG_YAML, experiment_id=experiment_id)


def test_extended_download(initialize_test_dir):
    json_file = test_directory / 'testfiles_elab' / 'downloaded_multiple_experiment.json'

    experiment = extended_download(save_to=json_file, server_config_json=SERVER_CONFIG_YAML,
                                   experiment_tags=['EEG_SUB2001'], format='csv',
                                   experiment_axis='columns')

    assert json_file.exists()
    for exp in experiment:
        assert 'extra_fields' in exp

    # cleanup
    json_file.unlink()
