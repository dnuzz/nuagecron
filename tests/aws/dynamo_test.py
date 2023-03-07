from moto import mock_lambda, mock_dynamodb

with mock_dynamodb():
    with mock_lambda():
        # This is here because a call chain instantiates a boto client
        from nuagecron.adapters.aws.adapters import dictionary_to_dynamo
from nuagecron.core.models.executions import ExecutionStatus


def test_update():
    update_dict = dictionary_to_dynamo(
        {"execution_status": {12345: ExecutionStatus.ready}}, True
    )
    assert "M" in update_dict["execution_status"]["Value"]
    assert update_dict["execution_status"]["Value"]["M"]
    assert update_dict["execution_status"]["Value"]["M"]["12345"]["S"] == "ready"


def test_update_multi():
    update_dict = dictionary_to_dynamo(
        {
            "execution_status": {
                12345: ExecutionStatus.ready,
                54321: ExecutionStatus.failed,
            }
        },
        True,
    )
    assert "M" in update_dict["execution_status"]["Value"]
    assert update_dict["execution_status"]["Value"]["M"]
    assert update_dict["execution_status"]["Value"]["M"]["12345"]["S"] == "ready"
    assert update_dict["execution_status"]["Value"]["M"]["54321"]["S"] == "failed"
