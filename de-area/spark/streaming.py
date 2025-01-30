from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType


#tripTypeColumn = (
#    F.when(
#        F.col('RateCodeId') == 1,
#        'SharedTrip'
#    )
#    .otherwise('SoloTrip')
#)

spark = (
            SparkSession
            .builder
            .appName('SparkCourse')
            .master('local[*]')
            .config('spark.dynamicAllocation.enabled', 'false')
            .getOrCreate()
    )

sc = spark.sparkContext

ride_schema = (
    StructType()
    .add('Id', 'integer')
    .add('VendorId', 'integer')
    .add('PickupTime', 'timestamp')
    .add('DropTime', 'timestamp')
    .add('PickupLocationId', 'integer')
    .add('DropLocationId', 'integer')
    .add('CabLicense', 'string')
    .add('DriverLicense', 'string')
    .add('PassengerCount', 'integer')
    .add('RateCodeId', 'integer')
)


input_df = (
    spark
    .readStream
    .schema(ride_schema)
    .option('maxFilesPerTrigger', 1)
    .option('multiline', 'true')
    .json('../data/taxi/Streaming/')
)

print('Is input_df streaming: {}'.format(input_df.isStreaming))

#console_query = (
#    input_df
#    .writeStream
#    .queryName('FhvRidesQuery')
#    .format('console')
#    .outputMode('append')
#    .trigger(processingTime='10 seconds')
#    .start()
#)

transformed_df = (
    input_df
    .select('Id', 'VendorId', 'PickupTime', 'DropTime',
            'DropLocationId', 'PassengerCount', 'RateCodeId')

    .where('PassengerCount > 0')
    .withColumn('TripTimeInMinutes',
                 F.round(
                    (F.unix_timestamp(F.col('DropTime')) 
                    - F.unix_timestamp(F.col('PickupTime'))) 
                    / 60

        )
    )
    #.withColumn('TripTime', tripTypeColumn)
    .drop('RateCodeId')
)


file_query = (
    transformed_df
    .writeStream
    .queryName('FhvRidesQuery')
    .format('csv')
    .option('path', '../data/taxi/Streaming/Transformed')
    .option('checkpointLocation', '../data/taxi/Streaming/Transformed/checkpoint')
    .outputMode('append')
    .trigger(processingTime='5 seconds')
    .start()
)


transformed_df.createOrReplaceTempView('FhvRides')

sql_df = spark.sql('''
            SELECT  
                   TripTime, TripTimeInMinutes, COUNT(*) AS TripCount Group
                 BY  DropLocationId, TripTime, TripTimeInMinutes
                   '''

)

sql_query = (
    sql_df
    .writeStream
    .queryName('FhvRidesQuery')
    .format('console')
    .outputMode('complete')
    .trigger(processingTime='5 seconds')
    .start()
)

sql_query.awaitTermination()


