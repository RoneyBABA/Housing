# LEARNINGS FROM THE PROJECT [Proj0]
        MANY VARIATIONS OF THE SAME QUERRY HAS BEEN TRIED IN THE CODE, WHICH MEANS DO EXPLORE THE CODE TO LEARN MORE

df.head()       ##df.head(10)
        It returns top 5 rows of the dataset and lets us know what type of data we are dealing with
        //  SELECT * FROM dataset
            limit 5;


df.tail()       ##df.tail(20)
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
        //  SELECT count(distinct (size)) from dataset;


# Lambda Function
        Lambda helps to write small, one liner function on the fly without the need of creating an actual one and worring about its syntax
        ex :    roney = lambda a, b : a+b
                print(roney(68,1))


# Multiple outputs in a single cell 
        Use comma between the commands
        ex: df3['bhk'].unique(), df3.drop(['size'], axis='columns'), df3.shape


df3.bhk > 20
        Gives us the boolean value for each row but,
df3[df3.bhak > 20]
        gives us all the columns of the row where bhk is above 20       


# Creating vs accessing the Column
        To create
                df4['price_per_sqft'] = df4['price']*100000/df4.['total_sqft']
        To Access
                df4.price_per_sqft = df4.price*100000//df4.total_sqft


# Number of distinct entries in a column
        df.col1.nunique                    OR
        len(df.col1.unique)


# Internal working
        df4[df4.price_per_sqft.max()] does not map because lets say:
        max() functions returns 2500, and df4[2500] may not be present in the dataset
        INSTEAD
                df4[df4.price_per_sqft == df4.price_per_sqft.max()]

        For Max and Min
                df.nlargest(5, 'col2')          df.nsmallest(6, 'col3')
# Sub Querries  
        loc_stats = df4.groupby('location')['location'].count()

        SQL
                SELECT * FROM dataset
                WHERE location IN (
                        SELECT location FROM dataset
                        GROUP BY location
                        HAVING COUNT(*) = 1
                );


# Observations
        df4.location.gropuby('location')['location'].count().sort_value(Ascending = False)
        CAN BE REPLACED WITH
        df4.location.value_counts()


# Observations
        // This is not possible
        outlier = df4[(df4.sqft_per_bhk<300) | (df4.sqft_per_bhk>2000)]
        df5 = df4[~outlier]

        // We have to use conditions. Either use it directly or store the condition in the variable.
        df5 = df4[~(df4.sqft_per_bhk<300) | (df4.sqft_per_bhk>2000)]
        cond = (df4.sqft_per_bhk<300) | (df4.sqft_per_bhk>2000)
        df5 = df4[~cond]


# Statistics Theory
        In a Normal Bell Curved Graph : mean = median = mode
        Standard Deviation (sd) = mean(distance of point from the mean)
        sd covers 68%, 2sd covers 95% and 3sd covers 99.7%.
        So in a banking transaction if a amount exceeds the value of 3sd, we get an notification. As an outlier is detected it can be a fraudulent payment.


# Observations
        df.att1.describe()
        Gives the important Mathematical Attributes of the Column. (mean, min, max, std)

        
# Dummy Variables & One Hot Encoding
        The model can't deal with Strings to train. We usually sub them with a number.
  CATEGORICAL VARIABLES
        Nominal
         These are String Variables which do not have any innate order. Ex: location, color.
         Suppose if DataSet consists of colors : Red, Blue, Yellow.
         If one encodes, Red = 1, Blue = 2, Yellow = 3.
         This might lead to flaweed conclusions : 1 + 2 = 3 or 1>2>3
                Hence, These types of variables are not associated with integers

        Ordinal
         Unlike Nominal variables, These variables have a heirachy in its structure.
         ex: Dissatisfied, Neutral, Satisfied

        Hence, TO ENCODE NOMINAL VARIABLES :
                We create multiple Dummy variables and encode em.
                   Color_Blue  Color_Green  Color_Red
                0           0            0          1
                1           1            0          0
                2           0            1          0
                3           0            0          1

# Dummy Variable Trap
        Equation for Multi Linear Regression :
                y = a0 + a1x1 + a2x2 .... anxn

        Here in the above example we can see : 
                Color_Red = 1 – (Color_Blue + Color_Green) //Color red column is redundant, and heance we can drop it.
                ex  : We have dropped 'others' column in the example, because if value of all the dummy variables is False, The location belongs to 'OTHERS'

        Also we know, to arrive at aforementioned equation we must :
               Res = Cross multiply (Transpose(M) X M)
               lets say det(Res) = 0. We can draw following conclusions :
                 1. That means the columns are perfectly correlated
                 2. When predictors are perfectly correlated, the matrix becomes singular (non-invertible)
                 3. This is a case of perfect multicollinearity.
        
        Regression needs to invert this matrix to solve for coefficients.
                Since it can’t invert, the solution is not unique → the model can’t decide which dummy variable gets what weight.

        We can simply consider (n-1) atrributes, to train our model. Any of the attributes can be dropped and just like int the example discuused above, a0 will componsate for it's absence. 


# Random State
        train_test_split(X,Y,test_size=0.2,random_state=10)
        The function randomly shuffles your data before splitting into train and test sets.
        random_state is just a seed value for the random number generator. (With same input, we get the same output)
        It is advisible because : 
                Reproducibility → in ML experiments, you want results to be consistent across runs.
                Debugging → easier if you can reproduce the same train/test split.x
                In research/assignments, reviewers can verify your results.


# Cross Validation and Shuffle split
        SHUFFLE SPLIT
        cvs = ShuffleSplit(n_splits=5, test_size=0.2, random_state =0)

        It uses random_state seed to randomize the dataset, and then splits the data into n_splits. Each split has it's own training and test dataset.

        K - Fold Cross Validation
        Idea is to Split the dataset into k folds (parts), train on k-1 folds and test on the remaining one, repeat until every fold has been used as test.

        Final score = average across all folds.

        CROSS VALIDATION
        cross_val_score(LinearRegression(), X, Y, cv=cvs)
        It runs the test on the selected model.
        It gives an array as output. They are accuracy of the model with respect to each split.


# Lasso Regression
        It performs better than the lineaar Regression on the test dataset, because linear Reg model tends to ovefit and the Lasso regression adds a penalty value to the regular regression. It is popularly used in for feature Selection.
        It makes the sure that as the value of Lamda grows, the atrributes which has weakest contribution to the model, is 0.