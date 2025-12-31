import java.io.IOException;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class AmazonReviewMapper
        extends Mapper<LongWritable, Text, Text, IntWritable> {

    private static final IntWritable ONE = new IntWritable(1); // Creates usable Hadoop integer object
    private Text polarityKey = new Text(); // stores sentiment polarity

    // Responsible for processing raw HDFS data
    @Override
    protected void map(LongWritable key, Text value, Context context)
            throws IOException, InterruptedException {

        // Each line: polarity, full_review
        String line = value.toString();
        String[] fields = line.split(",", 2);

        // Defensive check to ensure proper formatting of data
        if (fields.length == 2) {
            String polarity = fields[0].trim();
            polarityKey.set(polarity);
            context.write(polarityKey, ONE);
        }
    }
}

