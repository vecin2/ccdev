import pytest


def assert_file_matches_process(ced, process_path, process):
    loaded_process = ced.open(process_path)
    assert str(loaded_process) == str(process)


def test_when_creating_new_process_save_and_reopen_they_match(ced):
    process_path = "PRJContact.Implementation.Contact.InlineContact"
    process = ced.new_process(process_path)
    process.save()

    assert ced.get_realpath(process_path).exists()
    assert_file_matches_process(ced, process_path, process)


def test_open_product_process(product_ced, ced):
    """"When opening a process on the product repository should find it"""
    process_path = "CoreContactHistory.Implementation.Contact.Verbs.CreateContact"
    process = product_ced.new_process(process_path)
    process.save()
    ced.open(process_path)
    assert_file_matches_process(ced, process_path, process)


@pytest.mark.skip
def test_save_add_process_to_project():
    product_ced = CED("product")
    process_path = "PRJContactHistory.Implementation.Contact.Verbs.CreateContact"
    process = product_ced.new_process(process_path)
    process.save()
    assert process.realpath()
