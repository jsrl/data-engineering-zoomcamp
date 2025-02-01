CREATE OR REPLACE EXTERNAL TABLE `trips_data_all.fhv_tripdata`
OPTIONS (
  format = 'CSV',
  uris = ['gs://taxis-bucket-448121-i4/fhv/fhv_tripdata_2019-*.csv']
);
