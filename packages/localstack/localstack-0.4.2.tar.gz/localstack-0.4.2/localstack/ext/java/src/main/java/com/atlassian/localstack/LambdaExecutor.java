package com.atlassian.localstack;

import java.io.File;
import java.nio.ByteBuffer;
import java.util.Date;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import com.amazonaws.services.lambda.runtime.events.KinesisEvent;
import com.amazonaws.services.lambda.runtime.events.KinesisEvent.KinesisEventRecord;
import com.amazonaws.services.lambda.runtime.events.KinesisEvent.Record;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.apache.commons.codec.Charsets;
import org.apache.commons.io.FileUtils;
import org.apache.commons.lang3.StringUtils;

/**
 * TODO: Support for AWS Lambda functions written in Java is work in progress.
 *
 * @author Waldemar Hummer
 */
public class LambdaExecutor {

	@SuppressWarnings("unchecked")
	public static void main(String[] args) throws Exception {
		if(args.length < 2) {
			System.err.println("Usage: java " + LambdaExecutor.class.getSimpleName() +
					"<lambdaClass> <recordsFilePath>");
			boolean test = true;
			if(test) {
				final String testFile = "/tmp/test.event.kinesis.json";
				String content = "{\"records\": ["
						+ "{\"kinesis\": "
						+ "{}"
						+ "}"
						+ "]}";
				writeFile(testFile, content);
				args = new String[]{"com.atlassian.ForwardHandler", testFile};
				Runtime.getRuntime().addShutdownHook(new Thread() {
					public void run() {
						new File(testFile).delete();
					}
				});
			} else {
				System.exit(0);
			}
		}

		Class<RequestHandler<KinesisEvent, ?>> clazz = (Class<RequestHandler<KinesisEvent, ?>>) Class.forName(args[0]);
		RequestHandler<KinesisEvent, ?> handler = clazz.newInstance();
		KinesisEvent event = new KinesisEvent();
		ObjectMapper reader = new ObjectMapper();
		String fileContent = readFile(args[1]);
		@SuppressWarnings("deprecation")
		Map<String,Object> map = reader.reader(Map.class).readValue(fileContent);
		List<Map<String,Object>> records = (List<Map<String, Object>>) get(map, "Records");
		event.setRecords(new LinkedList<KinesisEvent.KinesisEventRecord>());
		for(Map<String,Object> record : records) {
			KinesisEventRecord r = new KinesisEventRecord();
			event.getRecords().add(r);
			Record kinesisRecord = new Record();
			Map<String,Object> kinesis = (Map<String, Object>) get(record, "Kinesis");
			kinesisRecord.setData(ByteBuffer.wrap(get(kinesis, "Data").toString().getBytes()));
			kinesisRecord.setPartitionKey((String) get(kinesis, "PartitionKey"));
			kinesisRecord.setApproximateArrivalTimestamp(new Date());
			r.setKinesis(kinesisRecord);
		}
		Context ctx = new LambdaContext();
		handler.handleRequest(event, ctx);
	}

	private static <T> T get(Map<String,T> map, String key) {
		T result = map.get(key);
		if(result != null) {
			return result;
		}
		key = StringUtils.uncapitalize(key);
		result = map.get(key);
		if(result != null) {
			return result;
		}
		return map.get(key.toLowerCase());
	}


	private static String readFile(String file) throws Exception {
		if(!file.startsWith("/")) {
			file = System.getProperty("user.dir") + "/" + file;
		}
		return FileUtils.readFileToString(new File(file), Charsets.UTF_8);
	}

	private static void writeFile(String file, String content) throws Exception {
		FileUtils.writeStringToFile(new File(file),content, Charsets.UTF_8);
	}

}
