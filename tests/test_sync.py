from sync_folder.main import Synchroniser
from pathlib import Path
from unittest.mock import MagicMock
import datetime as dt

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

def test_delete_file(tmp_path):

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

    #remove the test file
    test_file.unlink()

    #run the sync again
    app.run()

    #check the test file no longer exists in replica
    replica_file = test_replica / "test.txt"
    assert not replica_file.exists()

def test_scheduling(tmp_path):

    #init the test source
    test_source = tmp_path / "source"
    test_source.mkdir()

    #init the replica
    test_replica = tmp_path / "replica"
    test_replica.mkdir()

    #init the log file
    test_log = tmp_path / "sync.log"
    test_log.touch()


    #init the app
    app = Synchroniser(test_source, test_replica, 1, 3, test_log)

    #mock the sync_folder method
    app.sync_once = MagicMock()

    #run the syncs
    app.run()

    #check there were 3 calls
    assert app.sync_once.call_count == 3

def test_logging(tmp_path):

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

    #run once to create a file
    app.run()

    #modify the file
    test_file.write_text("modified")

    #run again to update the file
    app.run()

    #remove the file
    test_file.unlink()

    #run again to delete the file
    app.run()

    log_text = test_log.read_text()

    entries = log_text.splitlines()

    create_log, update_log, delete_log = entries

    #generate the timestamp
    timestamp = dt.datetime.now().replace(
            microsecond=0
            ).isoformat()

    assert "test.txt" in create_log
    assert "create" in create_log
    assert timestamp in create_log
    
    assert "test.txt" in update_log
    assert "update" in update_log
    assert timestamp in update_log

    assert "test.txt" in delete_log
    assert "delete" in delete_log
    assert timestamp in delete_log
