import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class AmazonReviewDriver {

    // Launches the custom MapReduce job
    public static void main(String[] args) throws Exception {

        // User should provide input and output paths
        if (args.length != 2) {
            System.err.println("Usage: AmazonReviewDriver <input> <output>");
            System.exit(-1);
        }

        // Configuring Hadoop environment
        Configuration conf = new Configuration();

        // Finding Java classes and assigning logics for MapReduce job
        Job job = Job.getInstance(conf, "Amazon Review Polarity Count");

        job.setJarByClass(AmazonReviewDriver.class);
        job.setMapperClass(AmazonReviewMapper.class);
        job.setReducerClass(AmazonReviewReducer.class);

        // Defining output datatypes (polarity: string, total count: integer)
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);

        // Reading input and transmitting output from and to HDFS
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}


