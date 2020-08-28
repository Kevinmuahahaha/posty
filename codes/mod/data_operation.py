from mod.modlog import debug, good, bad
import pymongo

server_usable=False
operating_db="db_name_test"
operating_collection="collection_name_test"
client = None

def revive_connection():
    global client
    client = pymongo.MongoClient("mongodb://localhost:27017",serverSelectionTimeoutMS=800) #800ms connection timout
    debug("Bringing up connection to DB.")
    try:
        client.server_info()
    except pymongo.errors.ServerSelectionTimeoutError as err:
        bad("Connection to DB Failed.")
        return False
    "Connection to DB Revived."
    return True


def touch( post_id, content ):
    global client
    if client == None:
        if not revive_connection():
            return "touch fail"
    debug("Storing data into db.")
    target_db = client[operating_db]
    target_collection = target_db[operating_collection]
    target_dict = {"postid":post_id}
    #check if reusing post-od
    if target_collection.find(target_dict).count() != 0:
        return "touch exist"
    target_dict = {"postid":post_id, "content":content}
    ret_data = target_collection.insert_one( target_dict )
    debug("Stored content to ID: " + str(ret_data.inserted_id))
    return "touch success"
    

def cat( post_id ):
    global client
    if client == None:
        if not revive_connection():
            return "cat fail"
    debug("Item being retrieved, at ID: " + str( post_id ))
    target_dict = {"postid":post_id}
    target_collection = client[operating_db][operating_collection]
    return target_collection.find_one(target_dict)


def rm( post_id ):
    global client
    if client == None:
        if not revive_connection():
            return "rm fail"
    debug("Item being removed, at ID: " + str(post_id))
    target_dict = {"postid":post_id}
    target_collection = client[operating_db][operating_collection]
    return target_collection.delete_one(target_dict).deleted_count

def ls( ):
    global client
    if client == None:
        if not revive_connection():
            return "ls fail"
    target_collection = client[operating_db][operating_collection]
    results = target_collection.find({},{"postid":1})
    return results
