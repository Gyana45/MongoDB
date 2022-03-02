import pymongo
import csv
import pandas as pd
from mycustomlogger import customlogger  # customlogger is the class name


# git test from github browser

class mongo_operation:
    log = customlogger.mylog("MongoTask.log")

    def __init__(self, url, db_name, col_name):
        """This will initialize connection
        :param url: connection url
        :param db_name: Database Name
        :param col_name: Collection Name
        """
        try:
            self.client = pymongo.MongoClient(str(url))
            self.db = self.create_database(db_name)
            self.col = self.create_collection(col_name)

            self.log.info("Connection created with Mongo db atlas")

        except Exception as e:
            self.log.exception(str(e))

    def create_database(self, db_name):
        """This will create a database
        :param db_name: Database name
        :return: Database
        """
        try:
            self.log.info("Creating database :" + str(db_name))
            self.db = self.client[str(db_name)]
            return self.db
        except Exception as e:
            self.log.exception(str(e))

    def create_collection(self, col_name):
        """This will create a collection in the database
        :param col_name: Collection Name
        :return: Collection
        """
        try:
            self.log.info("Creating Collection:" + str(col_name))
            self.col = self.db[str(col_name)]
            return self.col
        except Exception as e:
            self.log.exception(str(e))

    def show_databases(self):
        """This will show a list of available databases"""
        try:
            self.log.info("Listing all available Databases")
            db_list = self.client.list_database_names()
            self.log.info("Available Databases are: " + str(db_list))
            return db_list
        except Exception as e:
            self.log.exception(str(e))

    def insert_record(self, rec):
        """This will check record type and insert into collection
        :param rec: records(dict or list)
        """
        try:
            # if type(rec) == dict:
            if isinstance(rec, dict):
                self.log.info("Single record is present")
                self.col.insert_one(rec)
                self.log.info("Record inserted into Collection")
            # elif type(rec) == list:
            elif isinstance(rec, list):
                self.log.info("list of records are there to insert")
                self.col.insert_many(rec)
                self.log.info(str(len(rec)) + " records inserted into collection")

        except Exception as e:
            self.log.exception(str(e))

    def insert_from_csv(self, file_name):
        """This will fetch all records from csv file and store it into a list and insert into the collection
        :param file_name: csv file name"""
        try:
            self.log.info("Reading csv file")
            with open(file_name, 'r') as f:
                data = csv.reader(f, delimiter='\n')
                flag = True
                record_list = []
                for i in data:
                    if flag:
                        # for header list
                        header_list = i[0].split(';')
                        self.log.info("Columns of the csv file : " + str(header_list))
                        flag = False
                        continue
                    # records are in string format ,convert into list
                    rec = i[0].split(';')

                    # assigning header and corresponding value from csv file and store in a dictionary
                    record = {}
                    for m in range(len(header_list)):
                        record[header_list[m]] = rec[m]

                    # append the dictionary into list
                    record_list.append(record)

                self.insert_record(record_list)

        except Exception as e:
            self.log.exception(str(e))

    def find_one_record(self, query=None):
        """This will return one output based upon the query,if no query then one record from colllection.
        :param query : query given by user
        :return :single record"""

        try:
            if query:
                if isinstance(query, dict):
                    self.log.info("Query :" + str(query))
                    result = self.col.find_one(query)
                    return result
                else:
                    self.log.error("Error:Dictionary is passed in find_one_record method")
                    raise Exception(f"You have not entered a dictionary query: {query} in find_one_record method")
            else:
                self.log.info("No query selected")
                result = self.col.find_one()
                return result
        except Exception as e:
            self.log.exception(str(e))

    def find_all_record(self, query=None):
        """This will return all records based upon the query; if no query selected then all records in the collection
        :param query : query for fetching records (optional)
        :return :list of dictionary of all records
        """
        try:
            if query:
                if isinstance(query, dict):
                    result = self.col.find(query)
                    result_list = [i for i in result]
                    return result_list
                else:
                    self.log.error("Error: dictionary is not passed in the method")
                    raise Exception(f"You have not entered a dictionary query: {query} in find_all_record method")
            else:
                self.log.info("No query is selected")
                result_list = [i for i in self.col.find()]
                return result_list
        except Exception as e:
            self.log.exception(str(e))

    def find_limit_record(self, count=0):
        """This will fetch a certain limit of records
        :param count: limit of records(int)
        :return :list of dictionary of records
        """
        try:
            if isinstance(count, int):
                if count == 0:
                    # no limit given,means fetch all records
                    self.log.info("No count is given")
                    result_list = [i for i in self.col.find()]
                else:
                    self.log.info("Limit is :" + str(count))
                    result_list = [i for i in self.col.find().limit(count)]

                return result_list
            else:
                self.log.exception("limit value is other than integer value")
                raise Exception("limit value is other than integer value")
        except Exception as e:
            self.log.exception(str(e))

    def update_record_with_args(self, *args, **kwargs):
        """This will update data based on the filter condition
        :param args:first one will contail count,if count!=1 then update all"""
        try:
            count = int(args[0])
            present_data = args[1]
            new_data = args[2]
            self.log.info(
                "present data :" + str(present_data) + "  new data : " + str(new_data) + " count:" + str(count))

            if count != 1:
                # update all records
                self.col.update_many(present_data, {'$set': new_data})
            else:
                self.col.update_one(present_data, {'$set': new_data})
        except Exception as e:
            self.log.error("Error: " + str(e))

    def delete_one_record(self, query):
        """This will delete one record based on the query"""
        try:
            if isinstance(query, dict):
                total_rec = len([i for i in self.col.find()])
                count = len([i for i in self.col.find(query)])
                if count >= 1:
                    self.col.delete_one(query)
                    self.log.info("One record deleted.Available Records: " + str(total_rec - 1))
                else:
                    self.log.info("No Record is there to be deleted")
            else:
                self.log.error("Error: query type is not of dict")
                raise Exception("query type is not of dict")
        except Exception as e:
            self.log.error(str(e))

    def delete_many_records(self, query):
        """This will delete all records based on the query"""
        try:
            if isinstance(query, dict):
                total_rec = len([i for i in self.col.find()])
                count = len([i for i in self.col.find(query)])
                if count >= 1:
                    self.col.delete_many(query)
                    self.log.info(str(count) + " records deleted.Available Records: " + str(total_rec - count))
                else:
                    self.log.info("No Record is there to be deleted")
            else:
                self.log.error("Error: query type is not of dict")
                raise Exception("query type is not of dict")
        except Exception as e:
            self.log.error(str(e))

    def drop_collection(self):
        """This will drop the collection"""
        try:
            self.col.drop()
            self.log.info("Collection deleted")
            return "collection dropped"
        except Exception as e:
            self.log.error(str(e))

    def drop_database(self):
        try:
            self.client.drop_database(self.db)
            self.log.info("Database dropped")
            return "Database dropped"

        except Exception as e:
            self.log.error(str(e))
