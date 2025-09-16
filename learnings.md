# LEARNINGS FROM THE PROJECT [Proj0]

df.head()
        It returns top 5 rows of the dataset and lets us know what type of data we are dealing with
        //  SELECT * FROM dataset
            limit 5;

df.tail()
        Returns the bottom 5 entries in the table
        //  SELECT * FROM the dataset
            ORDER BY id DESC limit 5;

df1.groupby('area_type')['area_type'].agg('count')
        Gives the count of each type of entry in the coloumn
        //  SELECT area_type, count(area_type) as count from dataset
            GROUP BY area_type;

df1.shape
        Gives us the number of rows and coloumns present in the dataset
        //  SELECT
            (SELECT COUNT * from dataset) as TotalRows,
            (SLECT count * from INFORMATION_SCHEMA.COLUMNS WHEREE table_name="datset")

df2 = df1.drop(['bath','balcony','availability','society'],axis='columns')
        Drops unnecessary columns in the dataset
        //  ALTER TABLE dataset
            DROP COLUMN bath, DROP COLUMN balcony;

df2.isnull().sum()
        Counts the number of empty entries
        //  SELECT
                SUM(CASE WHEN price IS NULL THEN 1 ELSE 0 END) AS col1_nulls,
                SUM (CASE WHEN location IS NULL THEN 1 ELSE 0 END) as col2_nulls;

 df3['size'].unique
        Gives us the distincnt values in the column
        //  SELECT distinct(size) from dataset;

df3['size'].nunique
        Gives uds the number of unique values present
        //  SELECT count(distinct size ) from dataset;