1. Topics:

    1. Topic is a particular stream of data idetnefiable by name:
        - sequence of messages in a topic is called data stream
        - you can't query topics so you need to use kafka producers to send data and Kafka Consumers to read the data
    2. Topic is made of partitions(unlimited), wich are ordered and containing messages with ids called offset;
    3. Kafka topics are immutable once data is written in partition it can't be changed;
    4. Data is kept for limited amount of time(default a week)
    5. Order of messages is guaranteed only within partitin(not accrsosss partitions)
    6. Data is assigned randomly unless key is provided

2. Producers:
    - Producers write data to topics
    - Producers know which partition to write to(and which Kafka broker has it)

    1. Message 
        - Key - binary(nullable)
        - Value - binart(nullable)
        - Compression(none, gzip, snappy, lz4, zstd)
        Headers(KVP)
        - Partition + Offset
        - Timestamp

3. Consumer

~~~