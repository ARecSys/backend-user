from azure.storage.queue import ( QueueClient, BinaryBase64EncodePolicy, BinaryBase64DecodePolicy )
import base64
import os

def send_msg_to_queue ( user_public_id ):

    # Retrieve the connection string from an environment
    # variable named AZURE_STORAGE_CONNECTION_STRING
    connect_str = os.environ["AZURE_STORAGE_CONNECTION_STRING"]

    # Create a unique name for the queue
    q_name = "algofst"

    # Instantiate a QueueClient object which will
    # be used to create and manipulate the queue

    queue_client = QueueClient.from_connection_string(
                                connect_str, 
                                q_name,
                                message_encode_policy = BinaryBase64EncodePolicy(),
                                message_decode_policy = BinaryBase64DecodePolicy()
                            )

    message = user_public_id
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode( message_bytes )
    queue_client.send_message( base64_bytes )
