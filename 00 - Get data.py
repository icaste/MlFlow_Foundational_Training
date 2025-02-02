# Databricks notebook source
# MAGIC %run ./setup

# COMMAND ----------

dbutils.widgets.removeAll()
dbutils.widgets.dropdown("reset_all_data", "True", ["True", "False"])
dbutils.widgets.text("db_prefix", "churn_mlops", "Database Prefix")
dbutils.widgets.text("user_name", "odl_user_814792@databrickslabs.com", "User Name") # Place here your user name from set up or keep with this one 
dbutils.widgets.text("table_name", "telco_churn_ft", "Your Delta Table Name")

# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC ## Get Data
# MAGIC 
# MAGIC In the labs, we will assume that we the data is uploaded to this location: **/FileStore/mltraining/chrun_data/** 
# MAGIC ### Using the Data UI:
# MAGIC 
# MAGIC 1. Download the [data csv file](https://github.com/IBM/telco-customer-churn-on-icp4d/blob/master/data/Telco-Customer-Churn.csv) from github
# MAGIC 2. Upload data to DBFS in your workspace:
# MAGIC   * In production, it is highly recommended to upload the data to an adls location and mount it to the workspace. 
# MAGIC   * For simplicity and demo purpose, we will go simple & use the UI. Please refer to [the documentation](https://docs.microsoft.com/en-us/azure/databricks/data/data) for more details on how to upload data to dbfs. 

# COMMAND ----------

# MAGIC %md
# MAGIC ### Using command line

# COMMAND ----------

# DBTITLE 1,Download the file
# MAGIC %sh mkdir -p /FileStore/mltraining/churn_data; wget -O /FileStore/mltraining/churn_data/Telco-Customer-Churn.csv https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv

# COMMAND ----------

# DBTITLE 1,Create a DBFS data location 
# MAGIC %fs mkdirs /FileStore/mltraining/churn_data

# COMMAND ----------

# DBTITLE 1,Copy file to the DBFS data location
# MAGIC %fs cp file:/FileStore/mltraining/churn_data/Telco-Customer-Churn.csv dbfs:/FileStore/mltraining/churn_data/Telco-Customer-Churn.csv

# COMMAND ----------

# MAGIC %md
# MAGIC ### Check if the file exists
# MAGIC 
# MAGIC Regardless if the UI or command line option was used, the uploaded file should appear in **dbfs:/FileStore/mltraining20220621/churn_data/Telco-Customer-Churn.csv**

# COMMAND ----------

# DBTITLE 1,Check if the file exists
# MAGIC %fs ls /FileStore/mltraining/churn_data/

# COMMAND ----------

# MAGIC %md
# MAGIC 
# MAGIC ## Read data and store it in a delta table
# MAGIC 
# MAGIC #### Define variables and create a database

# COMMAND ----------

# DBTITLE 1,Please DO NOT change the variables values
# We assume the data csv file is located in teleco_churn_dataset as stated in the previous section
teleco_churn_dataset = "/FileStore/mltraining/churn_data/"

# COMMAND ----------

# MAGIC %md
# MAGIC #### Read data and store it in a managed delta table

# COMMAND ----------

table_name = dbutils.widgets.get("table_name") + "_" + dbutils.widgets.get("user_name")
print(f"Saving your table unde the name of {table_name}")
telco_df = spark.read.csv(teleco_churn_dataset, header="true", inferSchema="true")
telco_df.write.format("delta").mode("overwrite").saveAsTable(f"{dbName}.{table_name}")

# COMMAND ----------

# DBTITLE 1,Check table is created
display(spark.sql(f""" SELECT * FROM {dbName}.{table_name}"""))

# COMMAND ----------

# MAGIC %md-sandbox
# MAGIC &copy; 2022 Databricks, Inc. All rights reserved.<br/>Apache, Apache Spark, Spark and the Spark logo are trademarks of the <a href="http://www.apache.org/">Apache Software Foundation</a>.<br/><br/><a href="https://databricks.com/privacy-policy">Privacy Policy</a> | <a href="https://databricks.com/terms-of-use">Terms of Use</a> | <a href="http://help.databricks.com/">Support</a>
