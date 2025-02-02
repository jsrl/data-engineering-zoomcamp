CREATE TABLE `dbt_rosejos.green_tripdata`
AS SELECT * FROM `trips_data_all.green_tripdata`;

CREATE TABLE `dbt_rosejos.yellow_tripdata`
AS SELECT * FROM `trips_data_all.yellow_tripdata`;


CREATE TABLE `dbt_rosejos.fhv_tripdata`
AS SELECT * FROM `trips_data_all.fhv_tripdata`;
