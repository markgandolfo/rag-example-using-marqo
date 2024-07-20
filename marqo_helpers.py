from marqo.errors import MarqoWebError

#
# check if index exists already
# if not, create it
# return the name of the index
#
def find_or_create_index(mq, index_name):
    indexes = mq.get_indexes()
    if not _index_exists(indexes, index_name):
        try:
            mq.create_index(index_name)
        except MarqoWebError as e:
            print(f"Error creating the index: {e}")

    return index_name


def _index_exists(data, index_name):
    for item in data['results']:
        if item['indexName'] == index_name:
            return True
    return False


# 
# A shortcut for deleting all documents in an index
# This will delete and recreate the index
#
# would be nice to have a truncate() function built into marqo indstead
# 
def delete_all_recreate_index(mq, index_name):
    try:
        mq.delete_index(index_name)
    except MarqoWebError as e:
        print(f"Error deleting the index_name: {e}")

    try:
        mq.create_index(index_name)
    except MarqoWebError as e:
        print(f"Error creating the index: {e}")
    
    assert mq.index(index_name).get_stats()['numberOfDocuments'] == 0
