from __future__ import print_function

import sys


from pyspark.sql import SparkSession
from pyspark.sql.functions import explode
from pyspark.sql.functions import split
from pyspark.sql.functions import udf
from pyspark.sql.types import StructType, StringType, DoubleType,TimestampType
from pyspark.sql.functions import col,struct
from pyspark.sql.functions import from_json, to_json
from pyspark.sql.functions import window, current_timestamp,concat,lit
import spacy



if __name__ == "__main__":

    # Load the English language model
    nlp = spacy.load("en_core_web_sm")

    def extractMeaningfulWords(word):
        doc = nlp(word)
    
        # Check if any entity in the document contains the word
        for ent in doc.ents:
            if word in ent.text:
                return word

        return ""

    if len(sys.argv) != 7:
        print("""
        Usage: structured_kafka_wordcount.py <bootstrap-servers> <subscribe-type> <topics> <publishType> <publishTopic>
        """, file=sys.stderr)
        sys.exit(-1)

    bootstrapServers = sys.argv[1]
    subscribeType = sys.argv[2]
    topics = sys.argv[3]
    publishType = sys.argv[4]
    publishTopic = sys.argv[5]
    checkPointPath = sys.argv[6]

    spark = SparkSession\
        .builder\
        .appName("StructuredKafkaWordCount")\
        .getOrCreate()
    
    
    spark.conf.set("spark.sql.streaming.stateStore.stateSchemaCheck", "false")

    spark.sparkContext.setLogLevel("ERROR")

    schema = StructType() \
    .add("timestamp", TimestampType()) \
    .add("submission", StringType())

    # Create DataSet representing the stream of input lines from kafka
    lines = spark\
        .readStream\
        .format("kafka")\
        .option("kafka.bootstrap.servers", bootstrapServers)\
        .option(subscribeType, topics)\
        .option("failOnDataLoss", "false") \
        .load()\
        .selectExpr("CAST(value AS STRING)")

    words = lines.select(
        # explode turns each item in an array into a separate row
        explode(
            split(lines.value, " ")
        ).alias('word')
    )

    extract_meaningful_words_udf = udf(extractMeaningfulWords, StringType())

    # Generate running word count
    m_words = words.withColumn("meaningful_word", extract_meaningful_words_udf(col("word")))

    filtered_m_words = m_words.filter(m_words.meaningful_word != "")

    wordCounts = filtered_m_words.groupBy('meaningful_word').count()


    sortedCount = wordCounts.orderBy(wordCounts["count"].desc())   

    sortedCount = sortedCount.withColumn("kv", struct(col("meaningful_word"),col("count")))

    updated_sortedcount = sortedCount.withColumn("counted_value",to_json(col("kv")))

    query = (
        updated_sortedcount
        .selectExpr("CAST(counted_value AS STRING) AS value")
        .writeStream
        .outputMode('complete')
        .format("kafka")
        .option("kafka.bootstrap.servers", bootstrapServers)
        .option(publishType, publishTopic)
        .option("checkpointLocation", checkPointPath)
        .start()
    )

    query.awaitTermination()


    