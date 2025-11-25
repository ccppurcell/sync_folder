from sync_folder.main import Synchroniser
from pathlib import Path

def test_create_file(tmp_path):

    #init the test source
    test_source = tmp_path / "source"
    test_source.mkdir()

    #add a file to the test source
    (test_source / "test.txt").write_text("test")

    #init the replica
    test_replica = tmp_path / "replica"
    test_replica.mkdir()

    #init the log file
    test_log = tmp_path / "sync.log"
    test_log.touch()

    #init the app
    app = Synchroniser(test_source, test_replica, 0, 1, test_log)

    #run the sync
    app.run()

    #check the test file exists in replica
    replica_file = test_replica / "test.txt"
    assert replica_file.exists()

    #check test file contents
    assert replica_file.read_text() == "test"

def test_update_file(tmp_path):

    #init the test source
    test_source = tmp_path / "source"
    test_source.mkdir()

    #add a file to the test source
    test_file = test_source / "test.txt"
    test_file.write_text("test")

    #init the replica
    test_replica = tmp_path / "replica"
    test_replica.mkdir()

    #init the log file
    test_log = tmp_path / "sync.log"
    test_log.touch()

    #init the app
    app = Synchroniser(test_source, test_replica, 0, 1, test_log)

    #run sync once to get identical contents in the source and replica
    app.run()

    #modify the contents of the test file
    test_file.write_text("modified")

    #run sync again
    app.run()

    #check replica file was updated
    replica_file = test_replica / "test.txt"
    assert replica_file.read_text() == "modified"

